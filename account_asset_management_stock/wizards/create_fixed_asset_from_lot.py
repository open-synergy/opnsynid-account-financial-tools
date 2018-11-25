# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class CreateFixedAssetFromLot(models.TransientModel):
    _name = "stock.create_fixed_asset_from_lot"
    _description = "Create Fixed Asset From Lot"

    @api.model
    def _default_detail_ids(self):
        lot_ids = self._context.get("active_ids", [])
        obj_lot = self.env["stock.production.lot"]
        result = []
        for lot in obj_lot.browse(lot_ids):
            if lot.asset_id:
                continue
            product = lot.product_id
            categ = product.asset_category_id
            stock_move = lot._get_initial_move()
            if not stock_move:
                continue
            data = {
                "lot_id": lot.id,
                "stock_move_id": stock_move.id,
                "asset_category_id": categ and categ.id or False,
            }
            result.append((0, 0, data))
        return result

    detail_ids = fields.One2many(
        string="Serial Number",
        comodel_name="stock.create_fixed_asset_from_lot_detail",
        inverse_name="wizard_id",
        default=lambda self: self._default_detail_ids(),
    )

    @api.multi
    def button_create_asset(self):
        self.ensure_one()
        for detail in self.detail_ids.filtered(
                lambda r: r.asset_category_id):
            asset = detail._create_fixed_asset()
            detail.lot_id.write({
                "asset_id": asset.id,
            })


class CreateFixedAssetFromLotDetail(models.TransientModel):
    _name = "stock.create_fixed_asset_from_lot_detail"
    _description = "Create Fixed Asset From Lot Detail"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="stock.create_fixed_asset_from_lot",
    )
    lot_id = fields.Many2one(
        string="Serial Number",
        comodel_name="stock.production.lot",
    )
    stock_move_id = fields.Many2one(
        string="Initial Stock Move",
        comodel_name="stock.move",
    )
    asset_category_id = fields.Many2one(
        string="Asset Category",
        comodel_name="account.asset.category",
    )
    exception_message = fields.Char(
        string="Error Message",
    )
    parent_id = fields.Many2one(
        string="Parent Asset",
        comodel_name="account.asset.asset",
    )

    @api.multi
    def _create_fixed_asset(self):
        self.ensure_one()
        obj_asset = self.env["account.asset.asset"]
        return obj_asset.create(self._prepare_fixed_asset_data())

    @api.multi
    def _get_salvage_value(self, value=0.0):
        self.ensure_one()
        result = 0.0
        product = self.lot_id.product_id
        if product.fixed_asset_salvage_value_computation == "fixed":
            result = product.fixed_asset_salvage_value
        else:
            result = (100.00 / product.fixed_asset_salvage_value) * value
        return result

    @api.multi
    def _get_purchase_value(self):
        self.ensure_one()
        move = self.stock_move_id
        result = 0.0
        for lot in move.lot_ids.filtered(lambda r: r.id == self.lot_id.id):
            for quant in lot.quant_ids:
                result += quant.inventory_value
        return result

    @api.multi
    def _prepare_fixed_asset_data(self):
        self.ensure_one()
        lot = self.lot_id
        product = lot.product_id
        move = self.stock_move_id
        categ = self.asset_category_id
        picking = move.picking_id
        partner = picking.partner_id
        purchase_value = self._get_purchase_value()
        salvage_value = self._get_salvage_value(purchase_value)
        return {
            "name": product.name,
            "code": lot.name,
            "purchase_value": purchase_value,
            "salvage_value": salvage_value,
            "category_id": categ.id,
            "parent_id": self.parent_id and
            self.parent_id.id or False,
            "partner_id": partner and partner.id or False,
            "date_start": move.date,
            "method": categ.method,
            "type": "normal",
            "company_id": move.company_id.id,
            "method_number": categ.method_number,
            "method_period": categ.method_period,
            "method_progress_factor": categ.method_progress_factor,
            "method_time": categ.method_time,
            "prorata": categ.prorata,
            "lot_id": lot.id,
            "product_id": product.id,
        }

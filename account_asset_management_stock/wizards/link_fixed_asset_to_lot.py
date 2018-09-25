# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class LinkFixedAssetToLot(models.TransientModel):
    _name = "stock.link_fixed_asset_to_lot"
    _description = "Link Fixed Asset To Lot"

    @api.model
    def _default_detail_ids(self):
        asset_ids = self._context.get("active_ids", [])
        obj_asset = self.env["account.asset.asset"]
        result = []
        criteria = [
            ("product_id", "!=", False),
            ("lot_id", "=", False),
            ("id", "in", asset_ids),
            ("state", "=", "open"),
        ]
        for asset in obj_asset.search(criteria):
            data = {
                "asset_id": asset.id,
                "product_id": asset.product_id.id,
                "lot_id": False,
            }
            result.append((0, 0, data))
        return result

    detail_ids = fields.One2many(
        string="Serial Number",
        comodel_name="stock.link_fixed_asset_to_lot_detail",
        inverse_name="wizard_id",
        default=lambda self: self._default_detail_ids(),
    )

    @api.multi
    def button_link(self):
        self.ensure_one()
        for detail in self.detail_ids.filtered(lambda r: not r.lot_id):
            detail._link_fixed_asset_to_asset()
            detail._update_quant_value()


class LinkFixedAssetToLotDetail(models.TransientModel):
    _name = "stock.link_fixed_asset_to_lot_detail"
    _description = "Link Fixed Asset To Lot Detail"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="stock.link_fixed_asset_to_lot",
    )
    asset_id = fields.Many2one(
        string="Fixed Asset",
        comodel_name="account.asset.asset",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    lot_id = fields.Many2one(
        string="Serial Number",
        comodel_name="stock.production.lot",
    )

    @api.multi
    def _link_fixed_asset_to_asset(self):
        self.ensure_one()
        self.asset_id.write({
            "lot_id": self.lot_id.id,
        })
        self.lot_id.write({
            "asset_id": self.asset_id.id,
        })

    @api.multi
    def _update_quant_value(self):
        total_qty = 0.0
        for quant in self.lot_id.quant_ids:
            total_qty += quant.qty
        unit_price = self.asset_id.asset_value / total_qty
        self.lot_id.quant_ids.write({
            "cost": unit_price,
        })

# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def create(self, values):
        _super = super(StockQuant, self)
        result = _super.create(values)
        if (
            result.lot_id
            and result.product_id.auto_capitalization
            and result.cost > result.company_id.auto_capitalization_limit
            and result.product_id.asset_category_id
        ):
            result._create_fixed_asset()
        return result

    @api.multi
    def _get_salvage_value(self, value=0.0):
        self.ensure_one()
        result = 0.0
        product = self.lot_id.product_id
        if product.fixed_asset_salvage_value_computation == "fixed":
            result = product.fixed_asset_salvage_value
        else:
            result = (product.fixed_asset_salvage_value / 100.0) * value
        return result

    @api.multi
    def _create_fixed_asset(self):
        self.ensure_one()
        obj_asset = self.env["account.asset.asset"]
        obj_asset.create(self._prepare_fixed_asset_data())

    @api.multi
    def _get_asset_partner(self):
        self.ensure_one()
        move = self.history_ids[0]
        if move.picking_id.partner_id:
            return move.picking_id.partner_id
        else:
            return False

    @api.multi
    def _prepare_fixed_asset_data(self):
        self.ensure_one()
        product = self.product_id
        move = self.history_ids[0]  # TODO: Error prone?
        categ = product.asset_category_id
        partner = self._get_asset_partner()
        purchase_value = self.inventory_value
        salvage_value = self._get_salvage_value(purchase_value)
        return {
            "name": product.name,
            "code": self.lot_id.name,
            "purchase_value": purchase_value,
            "salvage_value": salvage_value,
            "category_id": categ.id,
            "parent_id": False,
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
            "lot_id": self.lot_id.id,
            "product_id": product.id,
        }

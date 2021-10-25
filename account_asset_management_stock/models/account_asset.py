# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    lot_id = fields.Many2one(
        string="Serial Number",
        comodel_name="stock.production.lot",
        ondelete="restrict",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )

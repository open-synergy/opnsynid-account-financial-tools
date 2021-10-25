# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    asset_category_id = fields.Many2one(
        string="Default Asset Category",
        comodel_name="account.asset.category",
    )
    fixed_asset_salvage_value_computation = fields.Selection(
        string="Fixed Asset Salvage Value Computation",
        selection=[
            ("fixed", "Fixed Value"),
            ("percent", "Percentage from Acquiring Cost"),
        ],
        default="fixed",
    )
    fixed_asset_salvage_value = fields.Float(
        string="Fixed Asset Salvage Value",
        default=0.0,
    )
    auto_capitalization = fields.Boolean(
        string="Auto Capitalization",
    )

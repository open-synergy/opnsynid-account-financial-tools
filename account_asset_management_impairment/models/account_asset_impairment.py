# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class FixedAssetImpairment(models.Model):
    _name = "account.asset.impairment"
    _description = "Fixed Asset Impairment"
    _inherit = ["account.asset.impairment_common"]
    _table = "account_asset_impairment"

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=False,
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args.append(("type", "=", "impairment"))
        return super(FixedAssetImpairment, self).search(
            args=args, offset=offset, limit=limit,
            order=order, count=count)

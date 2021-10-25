# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class FixedAssetImpairmentReversal(models.Model):
    _name = "account.asset.impairment_reversal"
    _description = "Fixed Asset Impairment Reversal"
    _inherit = ["account.asset.impairment_common"]
    _table = "account_asset_impairment"

    type = fields.Selection(
        default="reversal",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=False,
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args.append(("type", "=", "reversal"))
        return super(FixedAssetImpairmentReversal, self).search(
            args=args, offset=offset, limit=limit, order=order, count=count
        )

    @api.model
    def _get_sequence(self, company_id):
        company = self.env["res.company"].browse([company_id])[0]

        if company.fixed_asset_impairment_reversal_sequence_id:
            result = company.fixed_asset_impairment_reversal_sequence_id
        else:
            result = self.env.ref(
                "account_asset_management_impairment.sequence_"
                "fixed_asset_impairment_reversal"
            )
        return result

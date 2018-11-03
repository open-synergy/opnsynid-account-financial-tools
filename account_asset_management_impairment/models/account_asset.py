# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    @api.multi
    @api.depends(
        "impairment_ids", "impairment_ids.state"
    )
    def _compute_impairment(self):
        for asset in self:
            impairment = reversal = 0.0
            for imp in asset.impairment_ids.filtered(
                    lambda r: r.state == "valid"):
                impairment += imp.impairment_amount
            for rev in asset.impairment_reversal_ids.filtered(
                    lambda r: r.state == "valid"):
                reversal += imp.impairment_amount
            asset.amount_impairment = impairment - reversal

    impairment_ids = fields.One2many(
        string="Impairment",
        comodel_name="account.asset.impairment",
        inverse_name="asset_id",
        readonly=True,
    )
    impairment_reversal_ids = fields.One2many(
        string="Impairment Reversal",
        comodel_name="account.asset.impairment_reversal",
        inverse_name="asset_id",
        readonly=True,
    )
    amount_impairment = fields.Float(
        string="Impairment Value",
        compute="_compute_impairment",
    )

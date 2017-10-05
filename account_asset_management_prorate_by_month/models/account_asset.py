# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import datetime


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    prorate_by_month = fields.Boolean(
        string="Prorate by Month",
    )
    date_min_prorate = fields.Integer(
        string="Date Min. to Prorate",
        default=1,
    )

    @api.model
    def _get_fy_duration_factor(self, entry,
                                asset, firstyear):
        _super = super(AccountAsset, self)
        duration_factor = _super._get_fy_duration_factor(
            entry, asset, firstyear)
        if asset.prorata and asset.prorate_by_month:
            duration_factor = 1.0
            if firstyear:
                depreciation_date_start = datetime.strptime(
                    asset.date_start, '%Y-%m-%d')
                month_factor = 13 - depreciation_date_start.month
                if depreciation_date_start.day > asset.date_min_prorate:
                    month_factor -= 1
                duration_factor = float(month_factor) / 12.0
        return duration_factor

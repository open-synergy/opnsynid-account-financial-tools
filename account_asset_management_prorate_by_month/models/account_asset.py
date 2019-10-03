# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    prorate_by_month = fields.Boolean(
        string="Prorate by Month",
        default=True,
    )
    date_min_prorate = fields.Integer(
        string="Date Min. to Prorate",
        default=15,
    )

    @api.multi
    def _get_date_start(self):
        self.ensure_one()
        _super = super(AccountAsset, self)
        date_start = _super._get_date_start()
        dt_date_start = datetime.strptime(
            date_start,
            "%Y-%m-%d"
        )
        if self.prorate_by_month:
            if dt_date_start.day > self.date_min_prorate:
                dt_date_start = dt_date_start + relativedelta(day=1, months=1)

        return dt_date_start.strftime("%Y-%m-%d")

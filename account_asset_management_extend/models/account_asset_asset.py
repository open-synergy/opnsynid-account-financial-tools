# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta
from openerp import models, fields, api
from openerp.addons.decimal_precision import decimal_precision as dp


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    value_residual = fields.Float(
        compute="_compute_depreciation",
        digits=dp.get_precision("Account"),
        string="Residual Value",
        store=True,
    )
    value_depreciated = fields.Float(
        compute="_compute_depreciation",
        digits=dp.get_precision("Account"),
        string="Depreciated Value",
        store=True,
    )
    asset_value = fields.Float(
        compute="_asset_value",
        digits=dp.get_precision("Account"),
        string="Asset Value",
        store=True,
    )

    @api.multi
    def _get_asset_value(self):
        self.ensure_one()
        result = 0.0
        for field_dict in self._get_asset_value_field():
            if field_dict[0] == "+":
                result += getattr(self, field_dict[1])
            else:
                result -= getattr(self, field_dict[1])
        return result

    @api.model
    def _get_asset_value_field(self):
        return [
            ("+", "purchase_value"),
        ]

    @api.multi
    def _get_additional_depreciated_value(self):
        self.ensure_one()
        result = 0.0
        for field_dict in self._get_additional_depreciated_value_field():
            if field_dict[0] == "+":
                result += getattr(self, field_dict[1])
            else:
                result -= getattr(self, field_dict[1])
        return result

    @api.model
    def _get_additional_depreciated_value_field(self):
        return [
        ]

    @api.multi
    def _compute_line_dates(self, table, start_date, stop_date):
        """
        The posting dates of the accounting entries depend on the
        chosen 'Period Length' as follows:
        - month: last day of the month
        - quarter: last of the quarter
        - year: last day of the fiscal year

        Override this method if another posting date logic is required.
        """
        line_dates = []

        if self.method_period == 'month':
            line_date = start_date + relativedelta(day=31)
        if self.method_period == 'quarter':
            m = [x for x in [3, 6, 9, 12] if x >= start_date.month][0]
            line_date = start_date + relativedelta(month=m, day=31)
        elif self.method_period == 'year':
            line_date = table[0]['date_stop']

        i = 1
        while line_date < stop_date:
            line_dates.append(line_date)
            if self.method_period == 'month':
                line_date = line_date + relativedelta(months=1, day=31)
            elif self.method_period == 'quarter':
                line_date = line_date + relativedelta(months=3, day=31)
            elif self.method_period == 'year':
                line_date = table[i]['date_stop']
                i += 1

        # last entry
        if not (self.method_time == 'number' and
                len(line_dates) == self.method_number):
            line_dates.append(line_date)

        return line_dates

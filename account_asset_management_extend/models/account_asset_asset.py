# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta
from datetime import datetime
from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError

import logging
_logger = logging.getLogger(__name__)

try:
    import numpy as np
except (ImportError, IOError) as err:
    _logger.debug(err)


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    # TODO: Remove
    @api.multi
    @api.depends(
        "depreciation_line_ids",
        "depreciation_line_ids.line_date",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_check",
        "depreciation_line_ids.type",
    )
    def _compute_last_posted_depreciation_line(self):
        obj_line = self.env["account.asset.depreciation.line"]
        for asset in self:
            criteria = asset._prepare_valid_lines_domain()
            lines = obj_line.search(
                criteria, order="type desc, line_date desc")
            line_id = False
            if len(lines) > 0:
                line_id = lines[0].id
            asset.last_posted_depreciation_line_id = line_id

            criteria = asset._get_asset_value_line_domain()
            lines = obj_line.search(
                criteria, order="line_date desc, type desc")
            line_id = False
            if len(lines) > 0:
                line_id = lines[0].id
            asset.last_posted_asset_line_id = line_id

    @api.multi
    @api.depends(
        "method_time",
        "method_number",
        "method_period",
        "depreciation_line_ids",
        "depreciation_line_ids.line_date",
    )
    def _compute_method_period_number(self):
        for asset in self:
            method_period_start_number = method_period_depreciated_number = \
                method_period_remaining_number = 0.0
            asset_value = asset.last_posted_asset_value_id
            depreciation = asset.last_depreciation_id

            coef_method_time = asset._get_method_time_coefficient()
            coef_method_period = asset._get_method_period_coefficient()
            method_period_number = (coef_method_time / coef_method_period) * \
                asset.method_number
            np_date_unit = asset._get_numpy_date_unit()

            dt_asset_start_date = np.datetime64(
                asset.date_start,
                np_date_unit)

            if asset_value:
                dt_posted_asset_value_date = np.datetime64(
                    asset_value.line_date,
                    np_date_unit)
                dt_diff = dt_posted_asset_value_date - dt_asset_start_date
                method_period_start_number =\
                    asset.get_method_period_start_number(
                        dt_diff,
                        coef_method_period
                    )

            if depreciation and asset_value:
                # TODO: Pretty sure numpy has method to change string into dt
                dt_temp = datetime.strptime(
                    asset_value.line_date,
                    "%Y-%m-%d")
                dt_temp = dt_temp + relativedelta(day=1, days=-1)
                dt_temp = np.datetime64(dt_temp, np_date_unit)
                dt_depreciation = np.datetime64(
                    depreciation.line_date,
                    np_date_unit
                )
                method_period_depreciated_number = dt_depreciation - \
                    dt_temp

            method_period_remaining_number = method_period_number - \
                method_period_start_number - \
                method_period_depreciated_number

            asset.method_period_number = method_period_number
            asset.method_period_start_number = method_period_start_number
            asset.method_period_depreciated_number = \
                method_period_depreciated_number
            asset.method_period_remaining_number = \
                method_period_remaining_number

    @api.multi
    def get_method_period_start_number(
        self,
        dt_diff,
        coef_method_period
    ):
        self.ensure_one()
        result = 0
        if dt_diff and coef_method_period:
            result = int(dt_diff / coef_method_period)
        return result

    @api.multi
    @api.depends(
        "depreciation_line_ids",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_check",
        "depreciation_line_ids.type",
    )
    def _compute_asset_histories(self):
        obj_line = self.env["account.asset.depreciation.line"]
        for asset in self:
            last_posted_asset_value = \
                last_posted_depreciation = \
                last_posted_history = False

            posted_asset_value_domain = \
                asset._prepare_posted_asset_value_domain()
            posted_asset_values = obj_line.search(
                posted_asset_value_domain,
                order="line_date, type")

            if len(posted_asset_values) > 0:
                last_posted_asset_value = posted_asset_values[-1]

            posted_depreciation_domain = \
                asset._prepare_posted_depreciation_domain()
            posted_depreciations = obj_line.search(
                posted_depreciation_domain,
                order="line_date, type")

            if len(posted_depreciations) > 0:
                last_posted_depreciation = posted_depreciations[-1]

            posted_history_domain = \
                asset._prepare_posted_history_domain()
            posted_histories = obj_line.search(
                posted_history_domain,
                order="line_date, type")

            if len(posted_histories) > 0:
                last_posted_history = posted_histories[-1]

            unposted_history_domain = \
                asset._prepare_unposted_history_domain()
            unposted_histories = obj_line.search(
                unposted_history_domain,
                order="line_date, type")

            asset.posted_asset_value_ids = posted_asset_values.ids
            asset.last_posted_asset_value_id = last_posted_asset_value and \
                last_posted_asset_value.id or \
                False
            asset.posted_depreciation_ids = posted_depreciations.ids
            asset.last_depreciation_id = last_posted_depreciation and \
                last_posted_depreciation.id or \
                False
            asset.unposted_history_ids = unposted_histories.ids
            asset.posted_history_ids = posted_histories.ids
            asset.last_posted_history_id = last_posted_history and \
                last_posted_history.id or \
                False

    # TODO: Remove

    @api.multi
    @api.depends(
        "depreciation_line_ids",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_check",
        "depreciation_line_ids.type",
    )
    def _compute_posted_depreciation_line_ids(self):
        obj_line = self.env["account.asset.depreciation.line"]
        for asset in self:
            domain = asset._prepare_posted_lines_domain()
            posted_lines = obj_line.search(
                domain, order="line_date desc")
            asset.posted_depreciation_line_ids = posted_lines.ids

    value_residual = fields.Float(
        compute="_compute_depreciation",
        digits=False,
        string="Residual Value",
        store=True,
    )
    value_depreciated = fields.Float(
        compute="_compute_depreciation",
        digits=False,
        string="Depreciated Value",
        store=True,
    )
    # pylint: disable=locally-disabled, method-compute
    asset_value = fields.Float(
        compute="_asset_value",
        digits=False,
        string="Asset Value",
        store=True,
    )
    # TODO: Store?
    method_number = fields.Integer(
        string="Age",
        help="Age according to time method",
    )
    # TODO: Store?
    method_period_number = fields.Integer(
        string="Age Based On Period Lenght",
        compute="_compute_method_period_number",
    )
    # TODO: Store?
    method_period_start_number = fields.Integer(
        string="Age On Asset Value Date",
        compute="_compute_method_period_number",
    )
    # TODO: Store?
    method_period_depreciated_number = fields.Integer(
        string="Depreciated Age",
        compute="_compute_method_period_number",
    )
    # TODO: Store?
    method_period_remaining_number = fields.Integer(
        string="Remaining Age",
        compute="_compute_method_period_number",
    )
    # TODO: Remove
    last_posted_depreciation_line_id = fields.Many2one(
        string="Last Posted Depreciation Line",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_last_posted_depreciation_line",
    )
    # TODO: Remove
    last_posted_asset_line_id = fields.Many2one(
        string="Last Asset Value Depreciation Line",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_last_posted_depreciation_line",
    )
    # TODO: Remove
    posted_depreciation_line_ids = fields.Many2many(
        string="Posted Depreciation Lines",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_posted_depreciation_line_ids",
    )

    posted_asset_value_ids = fields.Many2many(
        string="Posted Asset Value Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    last_posted_asset_value_id = fields.Many2one(
        string="Last Posted Asset Value History",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    posted_depreciation_ids = fields.Many2many(
        string="Posted Depreciation Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    last_depreciation_id = fields.Many2one(
        string="Last Depreciation History",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    unposted_history_ids = fields.Many2many(
        string="Unposted Asset Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    posted_history_ids = fields.Many2many(
        string="Posted Asset Histories",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )
    last_posted_history_id = fields.Many2one(
        string="Last Posted History",
        comodel_name="account.asset.depreciation.line",
        compute="_compute_asset_histories",
    )

    @api.multi
    def _get_asset_value(self):
        """
        Dynamically add/subsstract asset value from list.
        List of fields and their sign will be provided by
        _get_asset_value_field method.
        This will allow modification for other fixed asset event
        (e.g improvement or impairment)
        """
        self.ensure_one()
        result = 0.0
        for field_dict in self._get_asset_value_field():
            if field_dict[0] == "+":
                result += getattr(self, field_dict[1])
            else:
                result -= getattr(self, field_dict[1])
        return result

    @api.multi
    def _get_date_start(self):
        self.ensure_one()
        return self.date_start

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

    @api.multi
    def _prepare_posted_lines_domain(self):
        self.ensure_one()
        date = self.last_posted_asset_line_id.line_date
        return [
            "&",
            "&",
            "|", ("move_check", "=", True),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
            ("type", "=", "depreciate"),
            ("line_date", ">=", date)
        ]

    @api.multi
    def _prepare_valid_lines_domain(self):
        self.ensure_one()
        return [
            "&",
            "|", ("move_check", "=", True),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _prepare_depreciated_lines_domain(self):
        self.ensure_one()
        return [
            "&",
            "&",
            "|", ("move_check", "=", True),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
            ("type", "=", "depreciate"),
        ]

    @api.multi
    def _prepare_old_lines_domain(self):
        self.ensure_one()
        return [
            ("asset_id", "=", self.id),
            ("type", "=", "depreciate"),
            ("move_id", "=", False),
            ("init_entry", "=", False),
        ]

    @api.multi
    def _get_method_time_coefficient(self):
        self.ensure_one()
        result = 0
        if self.method_time == "year":
            result = 12
        return result

    @api.multi
    def _get_method_period_coefficient(self):
        self.ensure_one()
        return 1

    @api.multi
    def _get_numpy_date_unit(self):
        self.ensure_one()
        return "M"

    @api.multi
    def _get_asset_value_line(self):
        self.ensure_one()
        result = False
        obj_line = self.env["account.asset.depreciation.line"]
        domain = self._get_asset_value_line_domain()
        lines = obj_line.search(domain)
        if len(lines) > 0:
            result = lines[0]
        return result

    @api.multi
    def _get_asset_value_line_domain(self):
        self.ensure_one()
        return [
            ("asset_id", "=", self.id),
            ("type", "=", "create"),
        ]

    @api.multi
    def _get_amount_to_depreciate(self):
        self.ensure_one()
        asset_value = self.last_posted_asset_line_id.remaining_value
        if self.method == "linear":
            return asset_value - self.salvage_value
        else:
            return asset_value

    @api.multi
    def _create_depreciation_lines(
            self, table, table_index_start, line_index_start):
        self.ensure_one()
        line_i_start = line_index_start
        table_i_start = table_index_start
        posted_lines = self.posted_depreciation_line_ids
        obj_line = self.env["account.asset.depreciation.line"]
        seq = len(posted_lines)
        # SPONGE
        depr_line = self.last_posted_history_id
        # depr_line = self.last_posted_depreciation_line_id

        # last_date = table[-1]["lines"][-1]["date"]
        depreciated_value = sum([l.amount for l in posted_lines])

        for entry in table[table_i_start:]:
            for line in entry["lines"][line_i_start:]:
                seq += 1
                name = self._get_depreciation_entry_name(seq)
                amount = line["amount"]

                if amount:
                    vals = {
                        "previous_id": depr_line.id,
                        "amount": amount,
                        "asset_id": self.id,
                        "name": name,
                        "line_date": line["date"].strftime("%Y-%m-%d"),
                        "init_entry": entry["init"],
                    }
                    depreciated_value += amount
                    depr_line = obj_line.create(vals)
                else:
                    seq -= 1
            line_i_start = 0

    @api.multi
    def _prepare_posted_asset_value_domain(self):
        self.ensure_one()
        return [
            ("type", "=", "create"),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _prepare_posted_depreciation_domain(self):
        self.ensure_one()
        return [
            "&",
            "&",
            "|",
            ("move_check", "=", True),
            ("init_entry", "=", True),
            ("type", "=", "depreciate"),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _prepare_posted_history_domain(self):
        self.ensure_one()
        return [
            "&",
            "|",
            ("move_check", "=", True),
            ("init_entry", "=", True),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _prepare_unposted_history_domain(self):
        self.ensure_one()
        return [
            ("move_check", "=", False),
            ("init_entry", "=", False),
            ("asset_id", "=", self.id),
        ]

    @api.multi
    def _compute_starting_depreciation_entry(self, table):
        self.ensure_one()
        # TODO: Use new helper field
        line_obj = self.env["account.asset.depreciation.line"]
        domain = self._prepare_posted_lines_domain()
        posted_lines = line_obj.search(
            domain, order="line_date desc")

        # TODO: Use new helper field
        last_line = self.last_posted_depreciation_line_id

        if (len(posted_lines) > 0):
            last_depreciation_date = datetime.strptime(
                last_line.line_date, "%Y-%m-%d")
            last_date_in_table = table[-1]["lines"][-1]["date"]
            if last_date_in_table <= last_depreciation_date:
                raise UserError(
                    _("The duration of the asset conflicts with the "
                      "posted depreciation table entry dates."))

            for table_i, entry in enumerate(table):
                # residual_amount_table = \
                #     entry["lines"][-1]["remaining_value"]
                if entry["date_start"] <= last_depreciation_date \
                        <= entry["date_stop"]:
                    break
            if entry["date_stop"] == last_depreciation_date:
                table_i += 1
                line_i = 0
            else:
                entry = table[table_i]
                date_min = entry["date_start"]
                for line_i, line in enumerate(entry["lines"]):
                    # residual_amount_table = line["remaining_value"]
                    if date_min <= last_depreciation_date <= line["date"]:
                        break
                    date_min = line["date"]
                if line["date"] == last_depreciation_date:
                    line_i += 1
            table_i_start = table_i
            line_i_start = line_i
        else:  # no posted lines
            table_i_start = 0
            line_i_start = 0

        return table_i_start, line_i_start

    def _delete_unposted_history(self):
        self.ensure_one()
        # TODO: Change into new helper field
        line_obj = self.env["account.asset.depreciation.line"]
        domain = self._prepare_old_lines_domain()
        old_lines = line_obj.search(domain)
        if old_lines:
            old_lines.unlink()

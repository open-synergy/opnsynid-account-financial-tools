# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import calendar
from datetime import datetime

from dateutil.relativedelta import relativedelta
from openerp import _, api, models
from openerp.addons.account_asset_management.account_asset import (
    account_asset_asset,
    account_asset_depreciation_line,
)
from openerp.exceptions import Warning as UserError


class DummyFy(object):
    def __init__(self, *args, **argv):
        for key, arg in argv.items():
            setattr(self, key, arg)


@api.multi
@api.depends(
    "asset_value",
    "depreciation_line_ids",
    "depreciation_line_ids.amount",
    "depreciation_line_ids.previous_id",
    "depreciation_line_ids.init_entry",
    "depreciation_line_ids.move_id",
    "child_ids",
    "child_ids.value_residual",
    "child_ids.value_depreciated",
    "child_ids.parent_id",
)
def _compute_depreciation(self):
    for asset in self:
        if asset.type == "normal":
            lines = asset.depreciation_line_ids.filtered(
                lambda l: l.type in ("depreciate", "remove")
                and (l.init_entry or l.move_check)
            )
            value_depreciated = (
                sum(rec.amount for rec in lines)
                + asset._get_additional_depreciated_value()
            )
            asset.value_residual = asset._get_asset_value() - value_depreciated
            asset.value_depreciated = value_depreciated
        else:
            value_residual = value_depreciated = 0.0
            for child in asset.child_ids:
                if child.state == "open" and child.type == "normal":
                    value_residual += child.value_residual
                    value_depreciated += child.value_depreciated
            asset.value_residual = value_residual
            asset.value_depreciated = value_depreciated


@api.multi
@api.depends(
    "purchase_value",
    "salvage_value",
    "type",
    "method",
    "child_ids",
    "child_ids.asset_value",
    "child_ids.parent_id",
)
def _asset_value(self):
    for asset in self:
        if asset.type == "view":
            asset_value = 0.0
            for child in asset.child_ids:
                if child.state == "open" and child.type == "normal":
                    asset_value += child.asset_value
            asset.asset_value = asset_value
        elif asset.method in ["linear-limit", "degr-limit"]:
            asset.asset_value = asset._get_asset_value()
        else:
            asset.asset_value = asset._get_asset_value()


@api.multi
def compute_depreciation_board(self):
    for asset in self:
        if asset.value_residual == 0.0:
            continue

        asset._delete_unposted_history()

        table = asset._compute_depreciation_table()
        if not table:
            continue

        # TODO: WTF this section for. What is the case
        # group lines prior to depreciation start period
        # depreciation_start_date = datetime.strptime(
        #     asset.last_posted_asset_line_id.line_date,
        #     "%Y-%m-%d")
        #
        # lines = table[0]["lines"]
        # lines1 = []
        # lines2 = []
        # flag = lines[0]["date"] < depreciation_start_date
        # for line in lines:
        #     if flag:
        #         lines1.append(line)
        #         if line["date"] >= depreciation_start_date:
        #             flag = False
        #     else:
        #         lines2.append(line)
        # if lines1:
        #     def group_lines(x, y):
        #         y.update({"amount": x["amount"] + y["amount"]})
        #         return y
        #     lines1 = [reduce(group_lines, lines1)]
        #     lines1[0]["depreciated_value"] = 0.0
        # table[0]["lines"] = lines1 + lines2

        # check table with posted entries and
        # recompute in case of deviation
        table_i_start, line_i_start = asset._compute_starting_depreciation_entry(table)

        # insert into account.asset.depreciation.line
        asset._create_depreciation_lines(table, table_i_start, line_i_start)

    return True


@api.multi
def _compute_depreciation_table(self):  # noqa: C901
    ctx = self._context.copy()

    table = []
    if self.method_time in ["year", "number"] and not self.method_number:
        return table

    ctx["company_id"] = self.company_id.id
    fy_obj = self.env["account.fiscalyear"].with_context(ctx)
    init_flag = False
    try:
        # SPONGE
        fy_id = fy_obj.find(self.last_posted_asset_line_id.line_date)
        # fy_id = fy_obj.find(self.date_start)
        fy = fy_obj.browse(fy_id)
        if fy.state == "done":
            init_flag = True
        fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
        fy_date_stop = datetime.strptime(fy.date_stop, "%Y-%m-%d")
    except:  # noqa: E722
        # The following logic is used when no fiscal year
        # is defined for the asset start date:
        # - We lookup the first fiscal year defined in the system
        # - The "undefined" fiscal years are assumed to be years
        #   with a duration equal to a calendar year
        first_fy = fy_obj.search(
            [("company_id", "=", self.company_id.id)], order="date_stop ASC", limit=1
        )
        first_fy_date_start = datetime.strptime(first_fy.date_start, "%Y-%m-%d")
        # SPONGE
        asset_date_start = datetime.strptime(
            self.last_posted_asset_line_id.line_date, "%Y-%m-%d"
        )
        # asset_date_start = datetime.strptime(self.date_start, "%Y-%m-%d")
        fy_date_start = first_fy_date_start
        if asset_date_start > fy_date_start:
            asset_ref = (
                self.code and "{} (ref: {})".format(self.name, self.code) or self.name
            )
            raise UserError(
                _(
                    "You cannot compute a depreciation table for an asset "
                    "starting in an undefined future fiscal year."
                    "\nPlease correct the start date for asset %s."
                )
                % asset_ref
            )
        while asset_date_start < fy_date_start:
            fy_date_start = fy_date_start - relativedelta(years=1)
        fy_date_stop = fy_date_start + relativedelta(years=1, days=-1)
        fy_id = False
        fy = DummyFy(
            date_start=fy_date_start.strftime("%Y-%m-%d"),
            date_stop=fy_date_stop.strftime("%Y-%m-%d"),
            id=False,
            state="done",
            dummy=True,
        )
        init_flag = True

    depreciation_start_date = self._get_depreciation_start_date(fy)
    depreciation_stop_date = self._get_depreciation_stop_date(depreciation_start_date)

    while fy_date_start <= depreciation_stop_date:
        table.append(
            {
                "fy_id": fy_id,
                "date_start": fy_date_start,
                "date_stop": fy_date_stop,
                "init": init_flag,
            }
        )
        fy_date_start = fy_date_stop + relativedelta(days=1)
        try:
            fy_id = fy_obj.find(fy_date_start)
            init_flag = False
        except:  # noqa : E722
            fy_id = False
        if fy_id:
            fy = fy_obj.browse(fy_id)
            if fy.state == "done":
                init_flag = True
            fy_date_stop = datetime.strptime(fy.date_stop, "%Y-%m-%d")
        else:
            fy_date_stop = fy_date_stop + relativedelta(years=1)

    # Step 1:
    # Calculate depreciation amount per fiscal year.
    # This is calculation is skipped for method_time != "year".
    digits = self.env["decimal.precision"].precision_get("Asset Depreciation")
    fy_residual_amount = amount_to_depr = self._get_amount_to_depreciate()

    i_max = len(table) - 1
    asset_sign = self._get_asset_value() >= 0 and 1 or -1

    line_dates = self._compute_line_dates(
        table, depreciation_start_date, depreciation_stop_date
    )

    for i, entry in enumerate(table):

        year_amount = self._compute_year_amount(amount_to_depr, fy_residual_amount)

        if i == i_max:
            if self.method == "degressive":
                year_amount = fy_residual_amount - self.salvage_value

        # raise UserError(str(year_amount))
        if self.method_period == "year":
            period_amount = year_amount
        elif self.method_period == "quarter":
            period_amount = year_amount / 4
        elif self.method_period == "month":
            period_amount = year_amount / 12

        if i == i_max:
            if self.method == "linear":
                fy_amount = fy_residual_amount
            else:
                fy_amount = fy_residual_amount - self.salvage_value
        else:
            firstyear = i == 0 and True or False
            fy_factor = self._get_fy_duration_factor(entry, self, firstyear)

            fy_amount = year_amount * fy_factor

        if asset_sign * (fy_amount - fy_residual_amount) > 0:
            fy_amount = fy_residual_amount

        period_amount = round(period_amount, digits)
        fy_amount = round(fy_amount, digits)

        entry.update(
            {
                "period_amount": period_amount,
                "fy_amount": fy_amount,
            }
        )

        fy_residual_amount -= fy_amount
        if round(fy_residual_amount, digits) == 0:
            break

    i_max = i
    table = table[: i_max + 1]

    # Step 2:
    # Spread depreciation amount per fiscal year
    # over the depreciation periods.
    self._compute_depreciation_table_lines(
        table, depreciation_start_date, depreciation_stop_date, line_dates
    )

    return table


@api.multi
def _get_depreciation_start_date(self, fy):
    """
    In case of "Linear": the first month is counted as a full month
    if the fiscal year starts in the middle of a month.
    """
    if self.prorata:
        depreciation_start_date = datetime.strptime(
            self.last_posted_asset_line_id.line_date, "%Y-%m-%d"
        )
        depreciation_start_date += relativedelta(day=1)
    else:
        fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
        depreciation_start_date = datetime(fy_date_start.year, fy_date_start.month, 1)
    return depreciation_start_date


@api.multi
def _get_depreciation_stop_date(self, depreciation_start_date):
    self.ensure_one()
    asset_start_date = datetime.strptime(self.date_start, "%Y-%m-%d")
    asset_start_date += relativedelta(day=1)
    depreciation_stop_date = asset_start_date + relativedelta(
        years=self.method_number, days=-1
    )
    return depreciation_stop_date


@api.multi
def _compute_depreciation_table_lines(
    self, table, depreciation_start_date, depreciation_stop_date, line_dates
):

    digits = self.env["decimal.precision"].precision_get("Asset Depreciation")
    asset_sign = self._get_asset_value() >= 0 and 1 or -1
    i_max = len(table) - 1
    remaining_value = self._get_amount_to_depreciate()
    depreciated_value = 0.0

    # raise UserError(str(table))

    for i, entry in enumerate(table):

        lines = []
        fy_amount_check = 0.0
        fy_amount = entry["fy_amount"]
        li_max = len(line_dates) - 1
        for li, line_date in enumerate(line_dates):

            if round(remaining_value, digits) == 0.0:
                break

            if line_date > min(entry["date_stop"], depreciation_stop_date) and not (
                i == i_max and li == li_max
            ):
                break

            if (
                self.method == "degr-linear"
                and asset_sign * (fy_amount - fy_amount_check) < 0
            ):
                break

            amount = entry.get("period_amount")

            # last year, last entry
            # Handle rounding deviations.
            if i == i_max and li == li_max:
                amount = remaining_value
                remaining_value = 0.0
            else:
                remaining_value -= amount

            fy_amount_check += amount
            line = {
                "date": line_date,
                "amount": amount,
                "depreciated_value": depreciated_value,
                "remaining_value": remaining_value,
            }
            lines.append(line)
            depreciated_value += amount

        # Handle rounding and extended/shortened FY deviations.
        #
        # Remark:
        # In account_asset_management version < 8.0.2.8.0
        # the FY deviation for the first FY
        # was compensated in the first FY depreciation line.
        # The code has now been simplified with compensation
        # always in last FT depreciation line.

        if round(fy_amount_check - fy_amount, digits) != 0:
            diff = fy_amount_check - fy_amount
            amount = amount - diff
            remaining_value += diff
            lines[-1].update(
                {
                    "amount": amount,
                    "remaining_value": remaining_value,
                }
            )
            depreciated_value -= diff

        if not lines:
            table.pop(i)
        else:
            entry["lines"] = lines
        line_dates = line_dates[li:]

    for _i, entry in enumerate(table):
        if not entry["fy_amount"]:
            entry["fy_amount"] = sum(rec["amount"] for rec in entry["lines"])


@api.multi
def _get_first_period_amount(self, table, entry, depreciation_start_date, line_dates):
    """
    Return prorata amount for Time Method "Year" in case of
    "Prorata Temporis"
    """
    amount = entry.get("period_amount")
    if self.prorata:
        dates = filter(lambda x: x <= entry["date_stop"], line_dates)
        full_periods = len(dates) - 1
        amount = entry["fy_amount"] - amount * full_periods
    return amount


@api.multi
def _compute_year_amount(self, amount_to_depr, residual_amount):
    """
    Localization: override this method to change the degressive-linear
    calculation logic according to local legislation.
    """
    if self.method_time != "year":
        raise UserError(
            _("Programming Error"),
            _(
                "The '_compute_year_amount' method is only intended for "
                "Time Method 'Number of Years.''"
            ),
        )

    year_amount_liner_divider = (
        self.method_period_number - self.method_period_start_number
    )
    year_amount_linear = (amount_to_depr / year_amount_liner_divider) * 12

    if self.method == "linear":
        return year_amount_linear

    year_amount_degressive = residual_amount * self.method_progress_factor

    if self.method == "degressive":
        return year_amount_degressive

    if self.method == "degr-linear":
        if year_amount_linear > year_amount_degressive:
            return min(year_amount_linear, residual_amount)
        else:
            return min(year_amount_degressive, residual_amount)

    raise UserError(_("Illegal value %s in asset.method.") % self.method)


@api.model
def _get_fy_duration_factor(self, entry, asset, firstyear):
    """
    localization: override this method to change the logic used to
    calculate the impact of extended/shortened fiscal years
    """
    duration_factor = 1.0
    fy_id = entry["fy_id"]
    if asset.prorata:
        if firstyear:
            depreciation_date_start = datetime.strptime(
                asset.last_posted_asset_line_id.line_date, "%Y-%m-%d"
            )
            first_fy_asset_days = depreciation_date_start + relativedelta(day=1)

            duration_factor = float(13 - first_fy_asset_days.month) / 12.0

        elif fy_id:
            duration_factor = asset._get_fy_duration(fy_id, option="years")
    elif fy_id:
        fy_months = asset._get_fy_duration(fy_id, option="months")
        duration_factor = float(fy_months) / 12
    return duration_factor


@api.model
def _get_fy_duration(self, fy_id, option="days"):
    """
    Returns fiscal year duration.
    @param option:
    - days: duration in days
    - months: duration in months,
              a started month is counted as a full month
    - years: duration in calendar years, considering also leap years
    """
    fy = self.env["account.fiscalyear"].browse(fy_id)
    fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
    fy_date_stop = datetime.strptime(fy.date_stop, "%Y-%m-%d")
    days = (fy_date_stop - fy_date_start).days + 1
    months = (
        (fy_date_stop.year - fy_date_start.year) * 12
        + (fy_date_stop.month - fy_date_start.month)
        + 1
    )
    if option == "days":
        return days
    elif option == "months":
        return months
    elif option == "years":
        year = fy_date_start.year
        cnt = fy_date_stop.year - fy_date_start.year + 1
        for i in range(cnt):
            cy_days = calendar.isleap(year) and 366 or 365
            if i == 0:  # first year
                if fy_date_stop.year == year:
                    duration = (fy_date_stop - fy_date_start).days + 1
                else:
                    duration = (datetime(year, 12, 31) - fy_date_start).days + 1
                factor = float(duration) / cy_days
            elif i == cnt - 1:  # last year
                duration = (fy_date_stop - datetime(year, 1, 1)).days + 1
                factor += float(duration) / cy_days
            else:
                factor += 1.0
            year += 1
        return factor


@api.model
@api.returns("self")
def create(self, vals):
    if vals.get("method_time") != "year" and not vals.get("prorata"):
        vals["prorata"] = True
    asset = super(account_asset_asset, self).create(vals)
    if self._context.get("create_asset_from_move_line"):
        # Trigger compute of depreciation_base
        asset.salvage_value = 0.0
    if asset.type == "normal":
        # create first asset line
        asset_line_obj = self.env["account.asset.depreciation.line"]
        line_name = asset._get_depreciation_entry_name(0)
        asset_date_start = asset._get_date_start()
        asset_line_vals = {
            "amount": asset.asset_value,
            "asset_id": asset.id,
            "name": line_name,
            "line_date": asset_date_start,
            "init_entry": True,
            "type": "create",
        }
        asset_line = asset_line_obj.create(asset_line_vals)
        if self._context.get("create_asset_from_move_line"):
            asset_line.move_id = self._context["move_id"]
    return asset


@api.multi
def _get_depreciation_entry_name(self, seq):
    """use this method to customise the name of the accounting entry"""
    return (self.code or str(self.id)) + "/" + str(seq)


@api.multi
@api.depends(
    "amount",
    "previous_id",
)
def _compute(self):
    for line in self:
        depreciated_value = remaining_value = 0.0

        previous_remaining_value = line.amount * 2.0
        previous_depreciated_value = -1.0 * line.amount
        previous_amount = line.amount

        if line.previous_id:
            previous_depreciated_value = line.previous_id.depreciated_value
            previous_amount = line.previous_id.amount
            if line.previous_id.type == "create":
                # previous_depreciated_value -= line.amount
                previous_amount = 0.0
            previous_remaining_value = line.previous_id.remaining_value

        depreciated_value = previous_depreciated_value + previous_amount
        remaining_value = previous_remaining_value - line.amount

        line.depreciated_value = depreciated_value
        line.remaining_value = remaining_value


class AccountAssetAssetMonkeypatch(models.TransientModel):
    _name = "account.asset.asset.monkeypatch"
    _description = "Asset Monkeypatch"

    def _register_hook(self, cr):
        account_asset_asset._compute_depreciation = _compute_depreciation
        account_asset_asset._asset_value = _asset_value
        account_asset_asset._compute_depreciation_table = _compute_depreciation_table
        account_asset_asset.compute_depreciation_board = compute_depreciation_board
        account_asset_asset._get_depreciation_start_date = _get_depreciation_start_date
        account_asset_asset._get_depreciation_stop_date = _get_depreciation_stop_date
        account_asset_asset._compute_depreciation_table_lines = (
            _compute_depreciation_table_lines
        )
        account_asset_asset._get_first_period_amount = _get_first_period_amount
        account_asset_asset._compute_year_amount = _compute_year_amount
        account_asset_asset._get_fy_duration_factor = _get_fy_duration_factor
        account_asset_asset.create = create
        account_asset_asset._get_depreciation_entry_name = _get_depreciation_entry_name
        account_asset_depreciation_line._compute = _compute
        _super = super(AccountAssetAssetMonkeypatch, self)
        return _super._register_hook(cr)

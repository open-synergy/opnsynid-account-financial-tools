# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, api, _
from openerp.addons.account_asset_management.\
    account_asset import account_asset_asset
from openerp.exceptions import Warning as UserError
from functools import reduce


class DummyFy(object):
    def __init__(self, *args, **argv):
        for key, arg in argv.items():
            setattr(self, key, arg)


@api.multi
@api.depends("asset_value",
             "depreciation_line_ids",
             "depreciation_line_ids.amount",
             "depreciation_line_ids.previous_id",
             "depreciation_line_ids.init_entry",
             "depreciation_line_ids.move_id")
def _compute_depreciation(self):
    for asset in self:
        if asset.type == "normal":
            lines = asset.depreciation_line_ids.filtered(
                lambda l: l.type in ("depreciate", "remove") and
                (l.init_entry or l.move_check))
            value_depreciated = sum([l.amount for l in lines]) + \
                asset._get_additional_depreciated_value()
            asset.value_residual = \
                asset._get_asset_value() - value_depreciated
            asset.value_depreciated = value_depreciated
        else:
            asset.value_residual = 0.0
            asset.value_depreciated = 0.0


@api.multi
@api.depends(
    "purchase_value", "salvage_value",
    "type", "method")
def _asset_value(self):
    for asset in self:
        if asset.type == "view":
            asset.asset_value = 0.0
        elif asset.method in ["linear-limit", "degr-limit"]:
            asset.asset_value = asset._get_asset_value()
        else:
            asset.asset_value = \
                asset._get_asset_value() - asset.salvage_value


@api.multi
def compute_depreciation_board(self):
    line_obj = self.env["account.asset.depreciation.line"]
    digits = self.env["decimal.precision"].precision_get("Account")

    for asset in self:
        if asset.value_residual == 0.0:
            continue
        domain = [
            ("asset_id", "=", asset.id),
            ("type", "=", "depreciate"),
            "|", ("move_check", "=", True), ("init_entry", "=", True)]
        posted_lines = line_obj.search(
            domain, order="line_date desc")
        if (len(posted_lines) > 0):
            last_line = posted_lines[0]
        else:
            last_line = line_obj
        domain = [
            ("asset_id", "=", asset.id),
            ("type", "=", "depreciate"),
            ("move_id", "=", False),
            ("init_entry", "=", False)]
        old_lines = line_obj.search(domain)
        if old_lines:
            old_lines.unlink()

        table = asset._compute_depreciation_table()
        if not table:
            continue

        # group lines prior to depreciation start period
        depreciation_start_date = datetime.strptime(
            asset.date_start, "%Y-%m-%d")
        lines = table[0]["lines"]
        lines1 = []
        lines2 = []
        flag = lines[0]["date"] < depreciation_start_date
        for line in lines:
            if flag:
                lines1.append(line)
                if line["date"] >= depreciation_start_date:
                    flag = False
            else:
                lines2.append(line)
        if lines1:
            def group_lines(x, y):
                y.update({"amount": x["amount"] + y["amount"]})
                return y
            lines1 = [reduce(group_lines, lines1)]
            lines1[0]["depreciated_value"] = 0.0
        table[0]["lines"] = lines1 + lines2

        # check table with posted entries and
        # recompute in case of deviation
        depreciated_value_posted = depreciated_value = 0.0
        if (len(posted_lines) > 0):
            last_depreciation_date = datetime.strptime(
                last_line.line_date, "%Y-%m-%d")
            last_date_in_table = table[-1]["lines"][-1]["date"]
            if last_date_in_table <= last_depreciation_date:
                raise UserError(
                    _("The duration of the asset conflicts with the "
                      "posted depreciation table entry dates."))

            for table_i, entry in enumerate(table):
                residual_amount_table = \
                    entry["lines"][-1]["remaining_value"]
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
                    residual_amount_table = line["remaining_value"]
                    if date_min <= last_depreciation_date <= line["date"]:
                        break
                    date_min = line["date"]
                if line["date"] == last_depreciation_date:
                    line_i += 1
            table_i_start = table_i
            line_i_start = line_i

            # check if residual value corresponds with table
            # and adjust table when needed
            depreciated_value_posted = depreciated_value = \
                sum([l.amount for l in posted_lines])
            residual_amount = asset.asset_value - depreciated_value
            amount_diff = round(
                residual_amount_table - residual_amount, digits)
            if amount_diff:
                # compensate in first depreciation entry
                # after last posting
                line = table[table_i_start]["lines"][line_i_start]
                line["amount"] -= amount_diff

        else:  # no posted lines
            table_i_start = 0
            line_i_start = 0

        seq = len(posted_lines)
        depr_line = last_line
        last_date = table[-1]["lines"][-1]["date"]
        depreciated_value = depreciated_value_posted
        for entry in table[table_i_start:]:
            for line in entry["lines"][line_i_start:]:
                seq += 1
                name = asset._get_depreciation_entry_name(seq)
                if line["date"] == last_date:
                    # ensure that the last entry of the table always
                    # depreciates the remaining value
                    if asset.method in ["linear-limit", "degr-limit"]:
                        depr_max = asset._get_asset_value() \
                            - asset.salvage_value
                    else:
                        depr_max = asset._get_asset_value()
                    amount = depr_max - depreciated_value
                else:
                    amount = line["amount"]
                if amount:
                    vals = {
                        "previous_id": depr_line.id,
                        "amount": amount,
                        "asset_id": asset.id,
                        "name": name,
                        "line_date": line["date"].strftime("%Y-%m-%d"),
                        "init_entry": entry["init"],
                    }
                    depreciated_value += amount
                    depr_line = line_obj.create(vals)
                else:
                    seq -= 1
            line_i_start = 0

    return True


@api.multi
def _compute_depreciation_table(self):
    ctx = self._context.copy()

    table = []
    if self.method_time in ["year", "number"] and not self.method_number:
        return table

    ctx["company_id"] = self.company_id.id
    fy_obj = self.env["account.fiscalyear"].with_context(ctx)
    init_flag = False
    try:
        fy_id = fy_obj.find(self.date_start)
        fy = fy_obj.browse(fy_id)
        if fy.state == "done":
            init_flag = True
        fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
        fy_date_stop = datetime.strptime(fy.date_stop, "%Y-%m-%d")
    except:
        # The following logic is used when no fiscal year
        # is defined for the asset start date:
        # - We lookup the first fiscal year defined in the system
        # - The "undefined" fiscal years are assumed to be years
        #   with a duration equal to a calendar year
        first_fy = fy_obj.search(
            [("company_id", "=", self.company_id.id)],
            order="date_stop ASC", limit=1)
        first_fy_date_start = datetime.strptime(
            first_fy.date_start, "%Y-%m-%d")
        asset_date_start = datetime.strptime(self.date_start, "%Y-%m-%d")
        fy_date_start = first_fy_date_start
        if asset_date_start > fy_date_start:
            asset_ref = self.code and "%s (ref: %s)" \
                % (self.name, self.code) or self.name
            raise UserError(
                _("You cannot compute a depreciation table for an asset "
                  "starting in an undefined future fiscal year."
                  "\nPlease correct the start date for asset %s.")
                % asset_ref)
        while asset_date_start < fy_date_start:
            fy_date_start = fy_date_start - relativedelta(years=1)
        fy_date_stop = fy_date_start + relativedelta(years=1, days=-1)
        fy_id = False
        fy = DummyFy(
            date_start=fy_date_start.strftime("%Y-%m-%d"),
            date_stop=fy_date_stop.strftime("%Y-%m-%d"),
            id=False,
            state="done",
            dummy=True)
        init_flag = True

    depreciation_start_date = self._get_depreciation_start_date(fy)
    depreciation_stop_date = self._get_depreciation_stop_date(
        depreciation_start_date)

    while fy_date_start <= depreciation_stop_date:
        table.append({
            "fy_id": fy_id,
            "date_start": fy_date_start,
            "date_stop": fy_date_stop,
            "init": init_flag})
        fy_date_start = fy_date_stop + relativedelta(days=1)
        try:
            fy_id = fy_obj.find(fy_date_start)
            init_flag = False
        except:
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
    digits = self.env["decimal.precision"].precision_get("Account")
    fy_residual_amount = self._get_asset_value()
    i_max = len(table) - 1
    asset_sign = self._get_asset_value() >= 0 and 1 or -1
    line_dates = self._compute_line_dates(
        table, depreciation_start_date, depreciation_stop_date)
    for i, entry in enumerate(table):

        if self.method_time == "year":
            year_amount = self._compute_year_amount(fy_residual_amount)
            if self.method_period == "year":
                period_amount = year_amount
            elif self.method_period == "quarter":
                period_amount = year_amount / 4
            elif self.method_period == "month":
                period_amount = year_amount / 12
            if i == i_max:
                if self.method in ["linear-limit", "degr-limit"]:
                    fy_amount = fy_residual_amount - self.salvage_value
                else:
                    fy_amount = fy_residual_amount
            else:
                firstyear = i == 0 and True or False
                fy_factor = self._get_fy_duration_factor(
                    entry, self, firstyear)
                fy_amount = year_amount * fy_factor
            if asset_sign * (fy_amount - fy_residual_amount) > 0:
                fy_amount = fy_residual_amount
            period_amount = round(period_amount, digits)
            fy_amount = round(fy_amount, digits)
        else:
            fy_amount = False
            if self.method_time == "number":
                number = self.method_number
            elif self.method_time == "end":
                number = len(line_dates)
            period_amount = round(self._get_asset_value() / number, digits)

        entry.update({
            "period_amount": period_amount,
            "fy_amount": fy_amount,
        })
        if self.method_time == "year":
            fy_residual_amount -= fy_amount
            if round(fy_residual_amount, digits) == 0:
                break
    i_max = i
    table = table[:i_max + 1]

    # Step 2:
    # Spread depreciation amount per fiscal year
    # over the depreciation periods.
    self._compute_depreciation_table_lines(
        table, depreciation_start_date, depreciation_stop_date,
        line_dates)

    return table


@api.multi
def _get_depreciation_start_date(self, fy):
    """
    In case of "Linear": the first month is counted as a full month
    if the fiscal year starts in the middle of a month.
    """
    if self.prorata:
        depreciation_start_date = datetime.strptime(
            self.date_start, "%Y-%m-%d")
    else:
        fy_date_start = datetime.strptime(fy.date_start, "%Y-%m-%d")
        depreciation_start_date = datetime(
            fy_date_start.year, fy_date_start.month, 1)
    return depreciation_start_date


@api.multi
def _get_depreciation_stop_date(self, depreciation_start_date):
    if self.method_time == "year":
        depreciation_stop_date = depreciation_start_date + \
            relativedelta(years=self.method_number, days=-1)
    elif self.method_time == "number":
        if self.method_period == "month":
            depreciation_stop_date = depreciation_start_date + \
                relativedelta(months=self.method_number, days=-1)
        elif self.method_period == "quarter":
            m = [x for x in [3, 6, 9, 12]
                 if x >= depreciation_start_date.month][0]
            first_line_date = depreciation_start_date \
                + relativedelta(month=m, day=31)
            months = self.method_number * 3
            depreciation_stop_date = first_line_date \
                + relativedelta(months=months - 1, days=-1)
        elif self.method_period == "year":
            depreciation_stop_date = depreciation_start_date + \
                relativedelta(years=self.method_number, days=-1)
    elif self.method_time == "end":
        depreciation_stop_date = datetime.strptime(
            self.method_end, "%Y-%m-%d")
    return depreciation_stop_date


@api.multi
def _compute_depreciation_table_lines(self, table, depreciation_start_date,
                                      depreciation_stop_date, line_dates):

    digits = self.env["decimal.precision"].precision_get("Account")
    asset_sign = self._get_asset_value() >= 0 and 1 or -1
    i_max = len(table) - 1
    remaining_value = self._get_asset_value()
    depreciated_value = 0.0

    for i, entry in enumerate(table):

        lines = []
        fy_amount_check = 0.0
        fy_amount = entry["fy_amount"]
        li_max = len(line_dates) - 1
        for li, line_date in enumerate(line_dates):

            if round(remaining_value, digits) == 0.0:
                break

            if (line_date > min(entry["date_stop"],
                                depreciation_stop_date) and not
                    (i == i_max and li == li_max)):
                break

            if self.method == "degr-linear" \
                    and asset_sign * (fy_amount - fy_amount_check) < 0:
                break

            if i == 0 and li == 0:
                amount = self._get_first_period_amount(
                    table, entry, depreciation_start_date, line_dates)
                amount = round(amount, digits)
            else:
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
        if self.method_time == "year":
            if round(fy_amount_check - fy_amount, digits) != 0:
                diff = fy_amount_check - fy_amount
                amount = amount - diff
                remaining_value += diff
                lines[-1].update({
                    "amount": amount,
                    "remaining_value": remaining_value,
                })
                depreciated_value -= diff

        if not lines:
            table.pop(i)
        else:
            entry["lines"] = lines
        line_dates = line_dates[li:]

    for i, entry in enumerate(table):
        if not entry["fy_amount"]:
            entry["fy_amount"] = sum(
                [l["amount"] for l in entry["lines"]])


@api.multi
def _get_first_period_amount(self, table, entry, depreciation_start_date,
                             line_dates):
    """
    Return prorata amount for Time Method "Year" in case of
    "Prorata Temporis"
    """
    amount = entry.get("period_amount")
    if self.prorata and self.method_time == "year":
        dates = filter(lambda x: x <= entry["date_stop"], line_dates)
        full_periods = len(dates) - 1
        amount = entry["fy_amount"] - amount * full_periods
    return amount


@api.multi
def _compute_year_amount(self, residual_amount):
    """
    Localization: override this method to change the degressive-linear
    calculation logic according to local legislation.
    """
    if self.method_time != "year":
        raise UserError(
            _("Programming Error"),
            _("The '_compute_year_amount' method is only intended for "
              "Time Method 'Number of Years.''"))

    year_amount_linear = self._get_asset_value() / self.method_number
    if self.method == "linear":
        return year_amount_linear
    if self.method == "linear-limit":
        if (residual_amount - year_amount_linear) < self.salvage_value:
            return residual_amount - self.salvage_value
        else:
            return year_amount_linear
    year_amount_degressive = residual_amount * \
        self.method_progress_factor
    if self.method == "degressive":
        return year_amount_degressive
    if self.method == "degr-linear":
        if year_amount_linear > year_amount_degressive:
            return min(year_amount_linear, residual_amount)
        else:
            return min(year_amount_degressive, residual_amount)
    if self.method == "degr-limit":
        if (residual_amount - year_amount_degressive) < self.salvage_value:
            return residual_amount - self.salvage_value
        else:
            return year_amount_degressive
    else:
        raise UserError(
            _("Illegal value %s in asset.method.") % self.method)


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
                asset.date_start, "%Y-%m-%d")
            fy_date_stop = entry["date_stop"]
            first_fy_asset_days = \
                (fy_date_stop - depreciation_date_start).days + 1
            if fy_id:
                first_fy_duration = asset._get_fy_duration(
                    fy_id, option="days")
                first_fy_year_factor = asset._get_fy_duration(
                    fy_id, option="years")
                duration_factor = \
                    float(first_fy_asset_days) / first_fy_duration \
                    * first_fy_year_factor
            else:
                first_fy_duration = \
                    calendar.isleap(entry["date_start"].year) \
                    and 366 or 365
                duration_factor = \
                    float(first_fy_asset_days) / first_fy_duration
        elif fy_id:
            duration_factor = asset._get_fy_duration(
                fy_id, option="years")
    elif fy_id:
        fy_months = asset._get_fy_duration(
            fy_id, option="months")
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
    months = (fy_date_stop.year - fy_date_start.year) * 12  \
        + (fy_date_stop.month - fy_date_start.month) + 1
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
                    duration = (
                        datetime(year, 12, 31) - fy_date_start).days + 1
                factor = float(duration) / cy_days
            elif i == cnt - 1:  # last year
                duration = (
                    fy_date_stop - datetime(year, 1, 1)).days + 1
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
        asset_line_vals = {
            "amount": asset.asset_value,
            "asset_id": asset.id,
            "name": line_name,
            "line_date": asset.date_start,
            "init_entry": True,
            "type": "create",
        }
        asset_line = asset_line_obj.create(asset_line_vals)
        if self._context.get("create_asset_from_move_line"):
            asset_line.move_id = self._context["move_id"]
    return asset


@api.multi
def _get_depreciation_entry_name(self, seq):
    """ use this method to customise the name of the accounting entry """
    return (self.code or str(self.id)) + "/" + str(seq)


class AccountAssetAssetMonkeypatch(models.TransientModel):
    _name = "account.asset.asset.monkeypatch"
    _description = "Asset Monkeypatch"

    def _register_hook(self, cr):
        account_asset_asset._compute_depreciation = \
            _compute_depreciation
        account_asset_asset._asset_value = \
            _asset_value
        account_asset_asset._compute_depreciation_table = \
            _compute_depreciation_table
        account_asset_asset.compute_depreciation_board = \
            compute_depreciation_board
        account_asset_asset._get_depreciation_start_date = \
            _get_depreciation_start_date
        account_asset_asset._get_depreciation_stop_date = \
            _get_depreciation_stop_date
        account_asset_asset._compute_depreciation_table_lines = \
            _compute_depreciation_table_lines
        account_asset_asset._get_first_period_amount = \
            _get_first_period_amount
        account_asset_asset._compute_year_amount = \
            _compute_year_amount
        account_asset_asset._get_fy_duration_factor = \
            _get_fy_duration_factor
        account_asset_asset.create = \
            create
        account_asset_asset._get_depreciation_entry_name = \
            _get_depreciation_entry_name
        _super = super(AccountAssetAssetMonkeypatch, self)
        return _super._register_hook(cr)

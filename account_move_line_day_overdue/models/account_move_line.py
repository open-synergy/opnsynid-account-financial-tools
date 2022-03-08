# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)
try:
    import numpy as np
    import pandas as pd
except (ImportError, IOError) as err:
    _logger.debug(err)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    _name = "account.move.line"

    days_overdue = fields.Integer(
        string="Days Overdue",
    )

    @api.model
    def compute_days_overdue(self):
        obj_ml = self.env["account.move.line"]
        criteria = [
            ("account_id.reconcile", "=", True),
            ("date_maturity", "!=", False),
            ("reconciled", "=", False),
        ]
        move_lines = obj_ml.search(criteria)
        for move_line in move_lines:
            move_line._compute_days_overdue()

    @api.multi
    def _compute_days_overdue(self):
        self.ensure_one()
        if self.date_maturity:
            dt_date_due = pd.to_datetime(self.date_maturity)
            dt_date_today = pd.datetime.now()
            if dt_date_today <= dt_date_due:
                day_diff = 0
            else:
                day_diff = int((dt_date_today - dt_date_due) / np.timedelta64(1, "D"))
            self.write({"days_overdue": day_diff})

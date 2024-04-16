# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    _name = "account.move.line"

    latest_reconciliation_date = fields.Date(
        string="Latest Reconciliation",
        compute="_compute_latest_reconciliation_date",
        store=True,
    )

    @api.depends(
        "matched_credit_ids",
        "matched_credit_ids.credit_move_id.date",
        "matched_debit_ids",
        "matched_debit_ids.debit_move_id.date",
    )
    def _compute_latest_reconciliation_date(self):
        AML = self.env["account.move.line"]
        for record in self:
            result = False
            aml_ids = set()
            aml_ids.update(record.mapped("matched_credit_ids.credit_move_id.id"))
            aml_ids.update(record.mapped("matched_debit_ids.debit_move_id.id"))
            if len(aml_ids) > 0:
                criteria = [
                    ("id", "in", sorted(aml_ids)),
                ]
                amls = AML.search(criteria)
                result = amls[0].date
            record.latest_reconciliation_date = result

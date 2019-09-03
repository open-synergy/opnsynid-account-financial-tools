# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    late_payment_penalty_type_ids = fields.Many2many(
        string="Applicable Late Payment Penalty Types",
        comodel_name="account.late_payment_penalty_type",
        relation="rel_aml_2_late_payment_penalty_type",
        column1="move_line_id",
        column2="late_payment_type_id",
    )

    @api.model
    def compute_late_payment_penalty(self):
        obj_ml = self.env["account.move.line"]
        criteria = [
            ("late_payment_penalty_type_ids", "!=", False),
            ("days_overdue", ">", 0),
        ]
        move_lines = obj_ml.search(criteria)
        for move_line in move_lines:
            move_line._create_late_payment_penalty()

    @api.multi
    def _create_late_payment_penalty(self):
        self.ensure_one()
        for penalty_type in self.late_payment_penalty_type_ids:
            if not penalty_type._trigger_auto_create(self):
                continue
            data = self._prepare_late_payment_penalty(penalty_type)
            if penalty_type.direction == "out":
                obj_name = "account.out_late_payment_penalty"
            else:
                obj_name = "account.in_late_payment_penalty"
            temp_record = self.env[obj_name].new(data)
            temp_record.onchange_journal_id()
            temp_record.onchange_account_id()
            temp_record.onchange_amount_base()
            temp_record.onchange_amount_residual()
            temp_record.onchange_date_due()
            temp_record.onchange_date_diff()
            temp_record.onchange_amount_penalty()
            values = temp_record._convert_to_write(temp_record._cache)
            temp_record = self.env[obj_name].create(values)

    @api.multi
    def _prepare_late_payment_penalty(self, penalty_type):
        self.ensure_one()
        return {
            "partner_id": self.partner_id.id,
            "type_id": penalty_type.id,
            "move_line_id": self.id,
            "date": fields.Date.today(),
        }

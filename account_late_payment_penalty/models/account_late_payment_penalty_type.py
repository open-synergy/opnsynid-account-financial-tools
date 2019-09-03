# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools.safe_eval import safe_eval as eval


class AccountLatePaymentPenaltyType(models.Model):
    _name = "account.late_payment_penalty_type"
    _description = "Late Payment Penalty Type"
    _order = "sequence, id"

    name = fields.Char(
        string="Late Payment Penalty Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    note = fields.Text(
        string="Note",
    )
    direction = fields.Selection(
        string="Direction",
        selection=[
            ("out", "Out"),
            ("in", "In"),
        ],
        required=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    journal_id = fields.Many2one(
        string="Default Journal",
        comodel_name="account.journal",
    )
    income_account_id = fields.Many2one(
        string="Income Account",
        comodel_name="account.account",
    )
    python_code = fields.Text(
        string="Code for Penalty Computation",
        default="result = 0.0",
    )
    auto_create_python_code = fields.Text(
        string="Code for Auto Create Penalty Creation",
        default="result = document.move_line_id.days_overdue > 0",
    )
    penalty_post_group_ids = fields.Many2many(
        string="Allow To Post Late Payment Penalty",
        comodel_name="res.groups",
        relation="rel_penalty_type_allowed_confirm_penalty",
        column1="penalty_type_id",
        column2="group_id",
    )
    penalty_cancel_group_ids = fields.Many2many(
        string="Allow To Cancel Late Payment Penalty",
        comodel_name="res.groups",
        relation="rel_penalty_type_allowed_cancel_penalty",
        column1="penalty_type_id",
        column2="group_id",
    )
    penalty_restart_group_ids = fields.Many2many(
        string="Allow To Restart Late Payment Penalty",
        comodel_name="res.groups",
        relation="rel_penalty_type_allowed_restart_penalty",
        column1="penalty_type_id",
        column2="group_id",
    )

    @api.multi
    def _get_localdict(self, document):
        return {
            "env": self.env,
            "self": self,
            "document": document,
        }

    @api.multi
    def _get_amount_penalty(self, document):
        self.ensure_one()
        localdict = self._get_localdict(document)
        try:
            eval(self.python_code,
                 localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        # pylint: disable=locally-disabled, do-not-use-bare-except
        except:
            result = 0.0
        return result

    @api.multi
    def _trigger_auto_create(self, document):
        self.ensure_one()
        localdict = self._get_localdict(document)
        try:
            eval(self.auto_create_python_code,
                 localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        # pylint: disable=locally-disabled, do-not-use-bare-except
        except:
            result = False
        return result

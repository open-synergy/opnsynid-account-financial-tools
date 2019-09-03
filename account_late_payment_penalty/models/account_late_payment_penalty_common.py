# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
import logging
_logger = logging.getLogger(__name__)
try:
    import pandas as pd
    import numpy as np
except (ImportError, IOError) as err:
    _logger.debug(err)


class AccountCommonLatePaymentPenalty(models.AbstractModel):
    _name = "account.common_late_payment_penalty"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _description = "Abstract Model for Late Payment Penalty"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    @api.model
    def _default_date(self):
        return fields.Date.today()

    @api.multi
    def _compute_policy(self):
        _super = super(AccountCommonLatePaymentPenalty, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_direction(self):
        for document in self:
            document.direction = False
            if document.type_id:
                document.direction = document.type_id.direction

    @api.multi
    def _compute_move_date_due(self):
        for document in self:
            document.move_date_due = document.move_line_id.date_maturity

    @api.multi
    def _compute_move_amount_base(self):
        for document in self:
            if document.direction == "out":
                document.move_amount_base = \
                    document.move_line_id.debit
            else:
                document.move_amount_base = \
                    document.move_line_id.credit

    @api.multi
    @api.depends(
        "partner_id",
        "type_id",
    )
    def _compute_allowed_move_line_ids(self):
        obj_aml = self.env["account.move.line"]
        for document in self:
            result = []
            if document.type_id and document.partner_id:
                criteria = [
                    ("partner_id", "=", document.partner_id.id),
                    ("account_id.reconcile", "=", True),
                    "|",
                    ("reconcile_id", "=", False),
                ]
                if document.direction == "out":
                    criteria.append(("debit", ">", 0.0))
                else:
                    criteria.append(("credit", ">", 0.0))
                result = [(6, 0, obj_aml.search(criteria).ids)]
            document.allowed_move_line_ids = result

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="account.late_payment_penalty_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    direction = fields.Selection(
        string="Direction",
        selection=[
            ("out", "Out"),
            ("in", "In"),
        ],
        compute="_compute_direction",
        store=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
        required=False,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_move_line_ids = fields.Many2many(
        string="Allowed Move Lines",
        comodel_name="account.move.line",
        compute="_compute_allowed_move_line_ids",
        store=False,
    )
    move_line_id = fields.Many2one(
        string="Move Line",
        comodel_name="account.move.line",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "general"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    account_id = fields.Many2one(
        string="Penalty Income Account",
        comodel_name="account.account",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        default=lambda self: self._default_date(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_due = fields.Date(
        string="Date Due",
        required=True,
        readonly=True,
    )
    move_date_due = fields.Date(
        string="Original Move Line Date Due",
        compute="_compute_move_date_due",
        store=True,
    )
    day_diff = fields.Integer(
        string="Day Diff",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_base = fields.Float(
        string="Base Amount",
        required=False,
        readonly=True,
        copy=False,
    )
    move_amount_base = fields.Float(
        string="Origin Move Base Amount",
        compute="_compute_move_amount_base",
        store=True,
    )
    amount_residual = fields.Float(
        string="Residual Amount",
        required=False,
        readonly=True,
        copy=False,
    )
    amount_penalty = fields.Float(
        string="Penalty Amount",
        copy=False,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    penalty_move_line_id = fields.Many2one(
        string="Penalty Move Line",
        comodel_name="account.move.line",
        copy=False,
        readonly=True,
    )
    penalty_move_id = fields.Many2one(
        string="Penalty Move",
        comodel_name="account.move",
        readonly=True,
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("post", "Post"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        copy=False,
        required=True,
        readonly=True,
    )
    # Policy Field
    post_ok = fields.Boolean(
        string="Can Post",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Unpost",
        compute="_compute_policy",
    )
    post_date = fields.Datetime(
        string="Post Date",
        copy=False,
        readonly=True,
    )
    post_user_id = fields.Many2one(
        string="Posted By",
        comodel_name="res.users",
        copy=False,
        readonly=True,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        copy=False,
        readonly=True,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        copy=False,
        readonly=True,
    )

    @api.multi
    def action_post(self):
        for document in self:
            document.write(document._prepare_post_data())
            document._reconcile_penalty()

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())
            document._unreconcile_aml()
            ml = document.penalty_move_line_id
            document.write({"penalty_move_line_id": False})
            ml.unlink()

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.multi
    def _prepare_post_data(self):
        self.ensure_one()
        move = self.env["account.move"].create(
            self._prepare_move_header()
        )
        if self.direction == "out":
            move_line = move.line_id.filtered(
                lambda r: r.account_id.id == self.move_line_id.account_id.id
                and r.debit > 0.0)[0]
        else:
            move_line = move.line_id.filtered(
                lambda r: r.account_id.id == self.move_line_id.account_id.id
                and r.credit > 0.0)[0]
        return {
            "state": "post",
            "post_date": fields.Datetime.now(),
            "post_user_id": self.env.user.id,
            "penalty_move_line_id": move_line.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "cancel_date": False,
            "cancel_user_id": False,
            "post_date": False,
            "post_user_id": False,
        }

    @api.multi
    def _prepare_move_header(self):
        self.ensure_one()
        period = self.env["account.period"].find(self.date)[0]
        data = {
            "ref": self.name,
            "date": self.date,
            "period_id": period.id,
            "journal_id": self.journal_id.id,
            "line_id": self._prepare_move_line(),
        }
        return data

    @api.multi
    def _prepare_move_line(self):
        self.ensure_one()
        result = []
        result.append((0, 0, self._prepare_debit_move_line()))
        result.append((0, 0, self._prepare_credit_move_line()))
        return result

    @api.multi
    def _get_debit_account_id(self):
        self.ensure_one()
        account_id = False
        if self.direction == "out":
            account_id = self.move_line_id.account_id.id
        else:
            account_id = self.account_id.id
        return account_id

    @api.multi
    def _get_credit_account_id(self):
        self.ensure_one()
        account_id = False
        if self.direction == "in":
            account_id = self.move_line_id.account_id.id
        else:
            account_id = self.account_id.id
        return account_id

    @api.multi
    def _prepare_debit_move_line(self):
        self.ensure_one()
        result = {
            "name": self.name,
            "debit": self.amount_penalty,
            "credit": 0.0,
            "account_id": self._get_debit_account_id(),
            "partner_id": self.partner_id.id,
            # TODO: Multi-currency support
        }
        return result

    @api.multi
    def _prepare_credit_move_line(self):
        self.ensure_one()
        result = {
            "name": self.name,
            "credit": self.amount_penalty,
            "debit": 0.0,
            "account_id": self._get_credit_account_id(),
            "partner_id": self.partner_id.id,
            # TODO: Multi-currency support
        }
        return result

    @api.multi
    def _reconcile_penalty(self):
        self.ensure_one()
        move_lines = self.move_line_id
        if self.move_line_id.reconcile_partial_id:
            move_lines = self.move_line_id.reconcile_partial_id.\
                line_partial_ids
        move_lines += self.penalty_move_line_id
        move_lines.reconcile_partial()

    @api.multi
    def _unreconcile_aml(self):
        self.ensure_one()
        move_line = self.penalty_move_line_id
        move_line.refresh()
        reconcile = move_line.reconcile_id or \
            move_line.reconcile_partial_id or \
            False
        if reconcile:
            move_lines = reconcile.line_id
            move_lines -= move_line
            reconcile.unlink()

            if len(move_lines) >= 2:
                move_lines.reconcile_partial()

    @api.onchange(
        "partner_id",
        "type_id",
    )
    def onchange_move_line_id(self):
        self.move_line_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id.journal_id:
            self.journal_id = self.type_id.journal_id

    @api.onchange(
        "move_line_id",
    )
    def onchange_amount_base(self):
        self.amount_base = 0.0
        if self.move_line_id:
            if self.direction == "out":
                self.amount_base = self.move_line_id.debit
            else:
                self.amount_base = self.move_line_id.credit

    @api.onchange(
        "move_line_id",
    )
    def onchange_amount_residual(self):
        self.amount_residual = 0.0
        if self.move_line_id:
            self.amount_residual = self.move_line_id.amount_residual

    @api.onchange(
        "move_line_id",
    )
    def onchange_date_due(self):
        self.date_due = False
        if self.move_line_id:
            self.date_due = self.move_line_id.date_maturity

    @api.onchange(
        "move_line_id",
        "type_id",
        "amount_base",
        "amount_residual",
        "day_diff",
    )
    def onchange_amount_penalty(self):
        self.amount_penalty = 0.0
        if self.move_line_id and self.type_id:
            self.amount_penalty = self.type_id._get_amount_penalty(self)

    @api.onchange(
        "type_id",
    )
    def onchange_account_id(self):
        self.account_id = False
        if self.type_id.income_account_id:
            self.account_id = self.type_id.income_account_id

    @api.onchange(
        "date",
        "date_due",
    )
    def onchange_date_diff(self):
        self.day_diff = 0
        if self.date and self.date_due:
            dt_date = pd.to_datetime(self.date)
            dt_date_due = pd.to_datetime(self.date_due)
            day_diff = int((dt_date - dt_date_due) / np.timedelta64(1, "D"))
            self.day_diff = day_diff

    @api.model
    def create(self, values):
        _super = super(AccountCommonLatePaymentPenalty, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write({
            "name": sequence,
        })
        return result

    @api.constrains(
        "move_amount_base",
        "amount_base",
    )
    def _restrict_amount_base_change(self):
        for document in self:
            if document.move_amount_base != document.amount_base:
                msg = _("Please delete late payment penaly first")
                raise UserError(msg)

    @api.constrains(
        "move_date_due",
        "date_due",
    )
    def _restrict_date_due_change(self):
        for document in self:
            if document.move_date_due != document.date_due:
                msg = _("Please delete late payment penaly first")
                raise UserError(msg)

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AccountCommonLatePaymentPenalty, self)
        _super.unlink()

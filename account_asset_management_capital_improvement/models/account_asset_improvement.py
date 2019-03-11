# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class FixedAssetImprovement(models.Model):
    _name = "account.asset_improvement"
    _description = "Fixed Asset Improvement"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common"
    ]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.model
    def _default_date_improvement(self):
        return fields.Datetime.now()

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(FixedAssetImprovement, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Document",
        required=True,
        readonly=True,
        default="/",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_improvement = fields.Date(
        string="Improvement Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default=lambda self: self._default_date_improvement(),
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="account.period",
        require=True,
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
        default=lambda self: self._default_company_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    asset_id = fields.Many2one(
        string="Asset",
        comodel_name="account.asset.asset",
        required=True,
        domain=[
            ("type", "=", "normal"),
            ("state", "=", "open")
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    asset_value_history_id = fields.Many2one(
        string="Asset Value History",
        comodel_name="account.asset.depreciation.line",
        readonly=True,
    )
    depreciation_history_id = fields.Many2one(
        string="Depreciation History",
        comodel_name="account.asset.depreciation.line",
        readonly=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self._default_currency_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    improvement_amount = fields.Float(
        string="Improvement Amount",
        required=True,
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    acc_move_id = fields.Many2one(
        string="Account Move",
        comodel_name="account.move",
        readonly=True,
    )
    depreciation_line_id = fields.Many2one(
        string="Depreciation Line",
        comodel_name="account.asset.depreciation.line",
        readonly=True,
    )
    acc_move_creation = fields.Selection(
        string="Acc. Move Creation",
        selection=[
            ("automatic", "Automatic"),
            ("manual", "Manual Selection"),
            ("workflow", "Workflow"),
        ],
        default="automatic",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False)
            ],
        },
    )
    exchange_account_id = fields.Many2one(
        string="Exchange Account",
        comodel_name="account.account",
        ondelete="restrict",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    accumulated_depreciation_account_id = fields.Many2one(
        string="Accumulated Depreciation Account",
        comodel_name="account.account",
        ondelete="restrict",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        required=True,
        readonly=True,
        track_visibility="onchange",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("valid", "Valid"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        copy=False,
    )
    confirmed_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirmed_user_id = fields.Many2one(
        string="Confirmation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    opened_date = fields.Datetime(
        string="Opened Date",
        readonly=True,
        copy=False,
    )
    opened_user_id = fields.Many2one(
        string="Open By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    validated_date = fields.Datetime(
        string="Validation Date",
        readonly=True,
        copy=False,
    )
    validated_user_id = fields.Many2one(
        string="Validation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancelled_date = fields.Datetime(
        string="Cancellation Date",
        readonly=True,
        copy=False,
    )
    cancelled_user_id = fields.Many2one(
        string="Cancellation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    open_ok = fields.Boolean(
        string="Can Open",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    valid_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )

    @api.multi
    def action_confirm(self):
        for improvement in self:
            improvement.write(self._prepare_confirm_data())

    @api.multi
    def action_open(self):
        for improvement in self:
            improvement.write(self._prepare_open_data())

    @api.multi
    def action_valid(self):
        for improvement in self:
            improvement.write(self._prepare_valid_data())
            improvement.asset_id.compute_depreciation_board()

    @api.multi
    def action_cancel(self):
        for improvement in self:
            # TODO: Change
            improvement.depreciation_line_id.unlink_move()
            improvement.depreciation_line_id.unlink()
            improvement.write(self._prepare_cancel_data())
            improvement.asset_id.compute_depreciation_board()

    @api.multi
    def action_restart(self):
        for improvement in self:
            improvement.write(self._prepare_restart_data())

    @api.multi
    def _prepare_asset_value(self):
        self.ensure_one()
        subtype_id = self.env.ref(
            "account_asset_management_capital_improvement."
            "depr_line_subtype_improvement")
        return {
            "name": self._get_asset_value_name(),
            "previous_id": self.asset_id.last_posted_depreciation_line_id.id,
            "subtype_id": subtype_id.id,
            "type": "create",
            "line_date": self.date_improvement,
            "amount": -1.0 * self.improvement_amount,
            "init_entry": True,
            "asset_id": self.asset_id.id,
        }

    @api.multi
    def _create_asset_value(self):
        self.ensure_one()
        obj_line = self.env["account.asset.depreciation.line"]
        asset_value = obj_line.create(self._prepare_asset_value())
        return asset_value

    @api.multi
    def _get_asset_value_name(self):
        self.ensure_one()
        name = "Asset value of %s" % (self.name)
        return name

    @api.multi
    def _create_adjustment_depreciation(self):
        self.ensure_one()
        if not self._check_create_adjustment():
            return False

        obj_line = self.env["account.asset.depreciation.line"]
        adj = obj_line.create(self._prepare_depreciation())
        adj.create_move()
        return adj

    @api.multi
    def _check_create_adjustment(self):
        self.ensure_one()
        if not self.asset_id.last_depreciation_id:

            return False

        if self.asset_id.last_depreciation_id.line_date == \
                self._get_depreciation_date().strftime("%Y-%m-%d"):
            return False

        return True

    @api.multi
    def _prepare_depreciation(self):
        self.ensure_one()
        subtype_id = self.env.ref(
            "account_asset_management_capital_improvement."
            "depr_line_subtype_improvement")
        return {
            "name": self._get_depreciation_name(),
            "subtype_id": subtype_id.id,
            "previous_id": self.asset_id.last_posted_depreciation_line_id.id,
            "type": "depreciate",
            "line_date": self._get_depreciation_date().strftime("%Y-%m-%d"),
            "amount": self._get_depreciation_amount(),
            "asset_id": self.asset_id.id,
        }

    @api.multi
    def _get_depreciation_name(self):
        self.ensure_one()
        name = "Depreciation adjustment of %s" % (self.name)
        return name

    @api.multi
    def _get_depreciation_date(self):
        self.ensure_one()
        dt_document = datetime.strptime(
            self.date_improvement,
            "%Y-%m-%d",
        )
        dt_depreciation = dt_document + relativedelta(day=1, days=-1)
        return dt_depreciation

    @api.multi
    def _get_depreciation_amount(self):
        self.ensure_one()

        table = self.asset_id._compute_depreciation_table()
        depreciation_date = self._get_depreciation_date()
        year_amount = 0.0

        for year in table:
            if year["date_start"] <= depreciation_date and \
                    year["date_stop"] >= depreciation_date:
                year_amount = year["fy_amount"]
                break

        coef = self._get_depreciation_date().month
        period_amount = year_amount / 12.0
        return coef * period_amount

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
            "confirmed_user_id": self.env.user.id,
            "confirmed_date": fields.Datetime.now(),
        }
        return result

    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        result = {
            "state": "open",
            "opened_user_id": self.env.user.id,
            "opened_date": fields.Datetime.now(),
        }
        return result

    @api.multi
    def _prepare_valid_data(self):
        self.ensure_one()
        acc_move = self._create_acc_move()
        depreciation = self._create_adjustment_depreciation()
        depreciation_id = depreciation and depreciation.id or False
        result = {
            "state": "valid",
            "acc_move_id": acc_move.id,
            "validated_user_id": self.env.user.id,
            "validated_date": fields.Datetime.now(),
            "asset_value_history_id": self._create_asset_value().id,
            "depreciation_history_id": depreciation_id,
        }
        return result

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        result = {
            "state": "cancel",
            "cancelled_user_id": self.env.user.id,
            "cancelled_date": fields.Datetime.now(),
            "asset_value_history_id": False,
            "depreciation_history_id": False,
        }
        return result

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
            "confirmed_user_id": False,
            "confirmed_date": False,
            "validated_user_id": False,
            "validated_date": False,
            "cancelled_user_id": False,
            "cancelled_date": False,
        }
        return result

    @api.onchange("date_improvement")
    def onchange_period_id(self):
        self.period_id = self.env[
            "account.period"].find(self.date_improvement).id

    @api.onchange("asset_id")
    def onchange_accumulated_depreciation_account(self):
        self.accumulated_depreciation_account_id = False
        if self.asset_id:
            self.accumulated_depreciation_account_id = \
                self.asset_id.category_id.account_depreciation_id

    @api.onchange("asset_id")
    def onchange_journal_id(self):
        self.journal_id = False
        if self.asset_id:
            self.journal_id = \
                self.asset_id.category_id.improvement_journal_id

    @api.model
    def create(self, values):
        _super = super(FixedAssetImprovement, self)
        result = _super.create(values)
        result.write({
            "name": result._create_sequence(),
        })
        return result

    @api.multi
    def _prepare_acc_move(self):
        self.ensure_one()
        move_lines = self._prepare_debit_move_line() + \
            self._prepare_credit_move_line()
        return {
            "name": self.name,
            "date": self.date_improvement,
            "period_id": self.period_id.id,
            "journal_id": self.journal_id.id,
            "line_id": move_lines,
        }

    @api.multi
    def _create_acc_move(self):
        self.ensure_one()
        return self.env["account.move"].create(
            self._prepare_acc_move()
        )

    @api.multi
    def _prepare_move_line(self, description, account, debit, credit):
        self.ensure_one()
        return [(0, 0, {
            "name": description,
            "account_id": account,
            "debit": debit,
            "credit": credit,
            "analytic_account_id": False,
        })]

    @api.multi
    def _prepare_debit_move_line(self):
        self.ensure_one()
        return self._prepare_move_line(
            description="Todo",
            account=self.accumulated_depreciation_account_id.id,
            debit=self.improvement_amount,
            credit=0.0,
        )

    @api.multi
    def _prepare_credit_move_line(self):
        self.ensure_one()
        return self._prepare_move_line(
            description="Todo",
            account=self.exchange_account_id.id,
            debit=0.0,
            credit=self.improvement_amount,
        )

    @api.multi
    def _create_depreciation_line(self, acc_move):
        self.ensure_one()
        obj_dpr_line = self.env["account.asset.depreciation.line"]
        return obj_dpr_line.create(
            self._prepare_depreciation_line(acc_move),
        )

    @api.multi
    def _prepare_depreciation_line(self, acc_move):
        self.ensure_one()
        subtype = self.env.ref(
            "account_asset_management_capital_improvement."
            "depr_line_subtype_improvement")
        return {
            "name": self.name,
            "previous_id": self._get_previous_depreciation_line_id(),
            "asset_id": self.asset_id.id,
            "line_date": self.date_improvement,
            "type": "depreciate",
            "move_id": acc_move.id,
            "amount": -1.0 * self.improvement_amount,
            "subtype_id": subtype.id,
        }

    @api.multi
    def _get_previous_depreciation_line_id(self):
        self.ensure_one()
        obj_dpr_line = self.env["account.asset.depreciation.line"]
        domain = [
            ("asset_id", "=", self.asset_id.id),
            ("type", "=", "depreciate"),
            "|",
            ("move_check", "=", True),
            ("init_entry", "=", True),
        ]
        results = obj_dpr_line.search(domain, order="line_date desc")
        if len(results) > 0:
            return results[0].id
        else:
            return False

# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class FixedAssetRetirementCommon(models.AbstractModel):
    _name = "account.asset_retirement_common"
    _description = "Abstract Model for Fixed Asset Retirement"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
    ]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.model
    def _default_date_disposition(self):
        return fields.Datetime.now()

    @api.model
    def _default_type_id(self):
        return False

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(FixedAssetRetirementCommon, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "acquisition_price",
        "disposition_price",
        "depreciated_amount",
    )
    def _compute_gain_loss(self):
        for retirement in self:
            retirement.gain_loss_amount = (
                retirement.disposition_price
                - retirement.acquisition_price
                + retirement.depreciated_amount
            )

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
    date_disposition = fields.Date(
        string="Disposition Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default=lambda self: self._default_date_disposition(),
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
        domain=[("type", "=", "normal"), ("state", "=", "open")],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="account.asset_retirement_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default=lambda self: self._default_type_id(),
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
    disposition_price = fields.Float(
        string="Disposition Price",
        required=True,
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    acquisition_price = fields.Float(
        string="Acquisition Price",
        required=True,
        readonly=True,
    )
    depreciated_amount = fields.Float(
        string="Depreciated Value",
        required=False,
        readonly=True,
    )
    gain_loss_amount = fields.Float(
        string="Gain/Loss Amount",
        compute="_compute_gain_loss",
        store=True,
    )
    exchange_acc_move_id = fields.Many2one(
        string="Exchange Account Move",
        comodel_name="account.move",
        readonly=True,
    )
    disposal_acc_move_id = fields.Many2one(
        string="Disposal Account Move",
        comodel_name="account.move",
        readonly=True,
    )
    gain_acc_move_id = fields.Many2one(
        string="Gain/Loss Account Move",
        comodel_name="account.move",
        readonly=True,
    )
    exchange_acc_move_creation = fields.Selection(
        string="Exchange Acc. Move Creation",
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
    disposal_acc_move_creation = fields.Selection(
        string="Disposal Acc. Move Creation",
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
    gain_acc_move_creation = fields.Selection(
        string="Gain/Loss Acc. Move Creation",
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
    exchange_journal_id = fields.Many2one(
        string="Exchange Journal",
        comodel_name="account.journal",
        readonly=True,
        required=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    disposal_journal_id = fields.Many2one(
        string="Disposal Journal",
        comodel_name="account.journal",
        readonly=True,
        required=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    gain_journal_id = fields.Many2one(
        string="Gain Journal",
        comodel_name="account.journal",
        readonly=True,
        required=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    asset_account_id = fields.Many2one(
        string="Asset Account",
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
    gain_account_id = fields.Many2one(
        string="Gain Account",
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
    loss_account_id = fields.Many2one(
        string="Loss Account",
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
        for retirement in self:
            retirement.write(self._prepare_confirm_data())

    @api.multi
    def action_open(self):
        for retirement in self:
            retirement.write(self._prepare_open_data())

    @api.multi
    def action_valid(self):
        for retirement in self:
            retirement.write(self._prepare_valid_data())
            retirement.asset_id.write(
                {
                    "state": "removed",
                }
            )

    @api.multi
    def action_cancel(self):
        for retirement in self:
            exchange_acc_move = self.exchange_acc_move_id
            disposal_acc_move = self.disposal_acc_move_id
            gain_acc_move = self.gain_acc_move_id
            retirement.write(self._prepare_cancel_data())
            exchange_acc_move.unlink()
            disposal_acc_move.unlink()
            gain_acc_move.unlink()
            retirement.asset_id.write(
                {
                    "state": "open",
                }
            )

    @api.multi
    def action_restart(self):
        for retirement in self:
            retirement.write(self._prepare_restart_data())

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
        exchange_acc_move = self._create_exchange_acc_move()
        disposal_acc_move = self._create_disposal_acc_move()
        gain_acc_move = self._create_gain_acc_move()
        result = {
            "state": "valid",
            "exchange_acc_move_id": exchange_acc_move.id,
            "disposal_acc_move_id": disposal_acc_move.id,
            "gain_acc_move_id": gain_acc_move.id,
            "validated_user_id": self.env.user.id,
            "validated_date": fields.Datetime.now(),
        }
        return result

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        result = {
            "state": "cancel",
            "cancelled_user_id": self.env.user.id,
            "cancelled_date": fields.Datetime.now(),
            "exchange_acc_move_id": False,
            "disposal_acc_move_id": False,
            "gain_acc_move_id": False,
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

    @api.onchange("date_disposition")
    def onchange_period_id(self):
        self.period_id = self.env["account.period"].find(self.date_disposition).id

    @api.onchange("asset_id")
    def onchange_acquisition_price(self):
        self.acquisition_price = 0.0
        if self.asset_id:
            self.acquisition_price = self.asset_id.purchase_value

    @api.onchange("asset_id")
    def onchange_depreciated_amount(self):
        self.depreciated_amount = 0.0
        if self.asset_id:
            self.depreciated_amount = self.asset_id.value_depreciated

    @api.onchange("asset_id", "type_id")
    def onchange_asset_account(self):
        self.asset_account_id = False
        if self.asset_id:
            self.asset_account_id = self.asset_id.category_id.account_asset_id

    @api.onchange("asset_id", "type_id")
    def onchange_exchange_account(self):
        self.exchange_account_id = False
        if self.type_id:
            self.exchange_account_id = self.type_id.exchange_account_id

    @api.onchange("asset_id", "type_id")
    def onchange_accumulated_depreciation_account(self):
        self.accumulated_depreciation_account_id = False
        if self.asset_id:
            self.accumulated_depreciation_account_id = (
                self.asset_id.category_id.account_depreciation_id
            )

    @api.onchange("asset_id", "type_id")
    def onchange_gain_account(self):
        self.gain_account_id = False
        if self.asset_id and self.asset_id.category_id.account_plus_value_id:
            self.gain_account_id = self.asset_id.category_id.account_plus_value_id
        elif self.type_id and self.type_id.gain_account_id:
            self.gain_account_id = self.type_id.gain_account_id

    @api.onchange("asset_id", "type_id")
    def onchange_loss_account(self):
        self.loss_account_id = False
        if self.asset_id and self.asset_id.category_id.account_min_value_id:
            self.loss_account_id = self.asset_id.category_id.account_min_value_id
        elif self.type_id and self.type_id.loss_account_id:
            self.loss_account_id = self.type_id.loss_account_id

    @api.onchange("asset_id", "type_id")
    def onchange_exchange_journal_id(self):
        self.exchange_journal_id = False
        if self.type_id:
            self.exchange_journal_id = self.type_id.exchange_journal_id

    @api.onchange("asset_id", "type_id")
    def onchange_disposal_journal_id(self):
        self.disposal_journal_id = False
        if self.type_id:
            self.disposal_journal_id = self.type_id.disposal_journal_id

    @api.onchange("asset_id", "type_id")
    def onchange_gain_journal_id(self):
        self.gain_journal_id = False
        if self.type_id:
            self.gain_journal_id = self.type_id.gain_journal_id

    @api.model
    def create(self, values):
        _super = super(FixedAssetRetirementCommon, self)
        result = _super.create(values)
        result.write(
            {
                "name": result._create_sequence(),
            }
        )
        return result

    @api.multi
    def _prepare_acc_move(self, journal, move_lines):
        self.ensure_one()
        return {
            "name": self.name,
            "date": self.date_disposition,
            "period_id": self.period_id.id,
            "journal_id": journal.id,
            "line_id": move_lines,
        }

    @api.multi
    def _prepare_exchange_acc_move(self):
        self.ensure_one()
        journal = self.exchange_journal_id
        move_lines = (
            self._prepare_exchange_debit_move_line()
            + self._prepare_exchange_credit_move_line()
        )
        return self._prepare_acc_move(journal, move_lines)

    @api.multi
    def _prepare_disposal_acc_move(self):
        self.ensure_one()
        journal = self.disposal_journal_id
        move_lines = (
            self._prepare_disposal_debit_move_line()
            + self._prepare_disposal_credit_move_line()
        )
        return self._prepare_acc_move(journal, move_lines)

    @api.multi
    def _prepare_gain_acc_move(self):
        self.ensure_one()
        journal = self.gain_journal_id
        move_lines = (
            self._prepare_gain_debit_move_line() + self._prepare_gain_credit_move_line()
        )
        return self._prepare_acc_move(journal, move_lines)

    @api.multi
    def _create_exchange_acc_move(self):
        self.ensure_one()
        return self.env["account.move"].create(self._prepare_exchange_acc_move())

    @api.multi
    def _create_disposal_acc_move(self):
        self.ensure_one()
        return self.env["account.move"].create(self._prepare_disposal_acc_move())

    @api.multi
    def _create_gain_acc_move(self):
        self.ensure_one()
        return self.env["account.move"].create(self._prepare_gain_acc_move())

    @api.multi
    def _prepare_exchange_move_line(self, description, account, debit, credit):
        self.ensure_one()
        return [
            (
                0,
                0,
                {
                    "name": description,
                    "account_id": account,
                    "debit": debit,
                    "credit": credit,
                    "analytic_account_id": False,
                },
            )
        ]

    @api.multi
    def _prepare_exchange_debit_move_line(self):
        self.ensure_one()
        return self._prepare_exchange_move_line(
            description="Todo",
            account=self.exchange_account_id.id,
            debit=self.disposition_price,
            credit=0.0,
        )

    @api.multi
    def _prepare_exchange_credit_move_line(self):
        self.ensure_one()
        return self._prepare_exchange_move_line(
            description="Todo",
            account=self.gain_account_id.id,
            debit=0.0,
            credit=self.disposition_price,
        )

    @api.multi
    def _prepare_disposal_debit_move_line(self):
        self.ensure_one()
        return self._prepare_exchange_move_line(
            description="Todo",
            account=self.accumulated_depreciation_account_id.id,
            debit=self.depreciated_amount,
            credit=0.0,
        )

    @api.multi
    def _prepare_disposal_credit_move_line(self):
        self.ensure_one()
        return self._prepare_exchange_move_line(
            description="Todo",
            account=self.asset_account_id.id,
            debit=0.0,
            credit=self.depreciated_amount,
        )

    @api.multi
    def _prepare_gain_debit_move_line(self):
        self.ensure_one()
        return self._prepare_exchange_move_line(
            description="Todo",
            account=self._get_gain_debit_account().id,
            debit=abs(self.gain_loss_amount),
            credit=0.0,
        )

    @api.multi
    def _prepare_gain_credit_move_line(self):
        self.ensure_one()
        return self._prepare_exchange_move_line(
            description="Todo",
            account=self._get_gain_credit_account().id,
            debit=0.0,
            credit=abs(self.gain_loss_amount),
        )

    @api.multi
    def _get_gain_debit_account(self):
        self.ensure_one()
        if self.gain_loss_amount >= 0.0:
            return self.gain_account_id
        else:
            return self.accumulated_depreciation_account_id

    @api.multi
    def _get_gain_credit_account(self):
        self.ensure_one()
        if self.gain_loss_amount < 0.0:
            return self.loss_account_id
        else:
            return self.accumulated_depreciation_account_id

# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from openerp import models, fields, api
from dateutil.relativedelta import relativedelta


class FixedAssetUsefulLifeEstimationChange(models.Model):
    _name = "account.asset_change_estimation_useful_life"
    _description = "Fixed Asset Useful Life Estimation Change"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
    ]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id

    @api.model
    def _default_date_change(self):
        return fields.Datetime.now()

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(FixedAssetUsefulLifeEstimationChange, self)
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
    date_change = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default=lambda self: self._default_date_change(),
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
    prev_method_number = fields.Integer(
        string="Previous Number of Years",
        required=True,
        readonly=True,
    )
    prev_method_period = fields.Selection(
        string="Previous Period Length",
        selection=[
            ("month", "Month"),
            ("quarter", "Quarter"),
            ("year", "Year"),
        ],
        required=True,
        readonly=True,
    )
    method_number = fields.Integer(
        string="Number of Years",
        required=True,
        default=1,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    method_period = fields.Selection(
        string="Period Length",
        selection=[
            ("month", "Month"),
            ("quarter", "Quarter"),
            ("year", "Year"),
        ],
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default="year",
        help="Period length for the depreciation accounting entries",
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
        for change in self:
            change.write(self._prepare_confirm_data())

    @api.multi
    def action_open(self):
        for change in self:
            change.write(self._prepare_open_data())

    @api.multi
    def action_valid(self):
        for change in self:
            change.write(self._prepare_valid_data())
            change.asset_id.write(
                self._prepare_asset_estimation_change()
            )
            change.asset_id.compute_depreciation_board()

    @api.multi
    def action_cancel(self):
        for change in self:
            change.write(self._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for change in self:
            change.write(self._prepare_restart_data())

    @api.multi
    def _prepare_asset_estimation_change(self):
        self.ensure_one()
        return {
            "method_number": self.method_number,
            "method_period": self.method_period,
        }

    @api.multi
    def _prepare_asset_value(self):
        self.ensure_one()
        subtype = self.env.ref(
            "account_asset_management_estimation_change."
            "depr_line_subtype_useful_life")
        return {
            "name": self._get_asset_value_name(),
            "subtype_id": subtype.id,
            "previous_id": self.asset_id.last_posted_depreciation_line_id.id,
            "type": "create",
            "line_date": self.date_change,
            "amount": 0.0,
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
        subtype = self.env.ref(
            "account_asset_management_estimation_change."
            "depr_line_subtype_useful_life")
        return {
            "name": self._get_depreciation_name(),
            "subtype_id": subtype.id,
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
            self.date_change,
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
        depreciation = self._create_adjustment_depreciation()
        depreciation_id = depreciation and depreciation.id or False
        result = {
            "state": "valid",
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

    @api.model
    def create(self, values):
        _super = super(FixedAssetUsefulLifeEstimationChange, self)
        result = _super.create(values)
        result.write({
            "name": result._create_sequence(),
        })
        return result

    @api.onchange("asset_id")
    def onchange_method_number(self):
        self.method_number = False
        if self.asset_id:
            self.method_number = self.asset_id.method_number

    @api.onchange("asset_id")
    def onchange_method_period(self):
        self.method_period = False
        if self.asset_id:
            self.method_period = self.asset_id.method_period

    @api.onchange("asset_id")
    def onchange_prev_method_number(self):
        self.prev_method_number = False
        if self.asset_id:
            self.prev_method_number = self.asset_id.method_number

    @api.onchange("asset_id")
    def onchange_prev_method_period(self):
        self.prev_method_period = False
        if self.asset_id:
            self.prev_method_period = self.asset_id.method_period

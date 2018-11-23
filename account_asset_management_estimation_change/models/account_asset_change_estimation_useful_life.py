# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, SUPERUSER_ID


class FixedAssetUsefulLifeEstimationChange(models.Model):
    _name = "account.asset_change_estimation_useful_life"
    _inherit = ["mail.thread", "base.sequence_document"]
    _description = "Fixed Asset Useful Life Estimation Change"

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
        for change in self:
            if change.company_id:
                company = change.company_id
                for policy in company.\
                        _get_asset_useful_life_button_policy_map():
                    if self.env.user.id == SUPERUSER_ID:
                        result = True
                    else:
                        result = company.\
                            _get_asset_useful_life_button_policy(
                                policy[1])
                    setattr(
                        change,
                        policy[0],
                        result,
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
        result = {
            "state": "valid",
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

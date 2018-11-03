# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, SUPERUSER_ID, _
from openerp.exceptions import Warning as UserError


class ComplexAssetMovementCommon(models.AbstractModel):
    _name = "account.complex_asset_movement_common"
    _inherit = ["mail.thread"]
    _description = "Common Object For Complex Fixed Asset Movement"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_date(self):
        return fields.Datetime.now()

    @api.model
    def _default_movement_type(self):
        return "add"

    @api.multi
    @api.depends(
        "state",
        "company_id",
    )
    def _compute_policy(self):
        for rec in self:
            rec.confirm_ok = rec.valid_ok = \
                rec.cancel_ok = \
                rec.restart_ok = False

            if self.env.user.id == SUPERUSER_ID:
                rec.confirm_ok = rec.valid_ok = \
                    rec.cancel_ok = \
                    rec.restart_ok = True
                continue

            if not rec.company_id:
                continue

            company = rec.company_id
            type = rec.movement_type
            for policy in company.\
                    _get_complex_asset_movement_button_policy_map(type):
                setattr(
                    rec,
                    policy[0],
                    company.
                    _get_complex_asset_movement_button_policy(
                        policy[1]),
                )

    name = fields.Char(
        string="# Order",
        required=True,
        default="/",
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
        default=lambda self: self._default_company_id(),
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
        required=False,
        readonly=True,
    )
    asset_id = fields.Many2one(
        string="Asset",
        comodel_name="account.asset.asset",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    parent_asset_id = fields.Many2one(
        string="Parent Asset",
        comodel_name="account.asset.asset",
        domain=[
            ("type", "=", "view"),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    movement_type = fields.Selection(
        string="Movement Type",
        selection=[
            ("add", "Add Asset to Parent Asset"),
            ("remove", "Remove Asset From Parent Asset")
        ],
        default=lambda self: self._default_movement_type(),
        required=True,
        readonly=True,
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
            ("valid", "Valid"),
            ("cancel", "Cancel"),
        ],
        default="draft",
        copy=False,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
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

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.write(self._prepare_confirm_data())

    @api.multi
    def action_valid(self):
        for rec in self:
            rec.write(self._prepare_valid_data())

    @api.multi
    def action_cancel(self):
        for rec in self:
            rec.write(self._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for rec in self:
            rec.write(self._prepare_restart_data())

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

    @api.multi
    def _prepare_post_create_data(self):
        self.ensure_one()
        result = {
            "name": self._create_sequence(),
        }
        return result

    @api.multi
    def _get_sequence(self):
        return False

    @api.multi
    def _create_sequence(self):
        self.ensure_one()
        name = self.name
        if self.name == "/":
            name = self.env["ir.sequence"].\
                next_by_id(self._get_sequence().id) or "/"
        return name

    @api.model
    def create(self, values):
        result = super(ComplexAssetMovementCommon, self).create(values)
        result.write(result._prepare_post_create_data())
        return result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for imp in self:
            if imp.state != "draft":
                if not self._context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(ComplexAssetMovementCommon, self)
        _super.unlink()

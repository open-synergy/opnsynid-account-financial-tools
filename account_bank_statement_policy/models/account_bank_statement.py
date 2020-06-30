# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class AccountBankStatement(models.Model):
    _name = "account.bank.statement"
    _inherit = [
        "account.bank.statement",
        "base.workflow_policy_object",
    ]

    @api.multi
    def _compute_policy(self):
        _super = super(AccountBankStatement, self)
        _super._compute_policy()

    # Policy Field
    reconcile_ok = fields.Boolean(
        string="Can Reconcile",
        compute="_compute_policy",
    )
    close_ok = fields.Boolean(
        string="Can Close",
        compute="_compute_policy",
    )
    open_ok = fields.Boolean(
        string="Can Open",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )

    # Log Fields
    reconcile_date = fields.Datetime(
        string="Reconcile Date",
        readonly=True,
        copy=False,
    )
    reconcile_user_id = fields.Many2one(
        string="Reconcile By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    close_date = fields.Datetime(
        string="Close Date",
        readonly=True,
        copy=False,
    )
    close_user_id = fields.Many2one(
        string="Close By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

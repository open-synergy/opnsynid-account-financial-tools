# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class FixedAssetRetirementType(models.Model):
    _name = "account.asset_retirement_type"
    _inherit = ["mail.thread"]
    _description = "Fixed Asset Retirement Type"

    name = fields.Char(
        string="Retirement Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    set_disposition_price = fields.Boolean(
        string="Allow To Set Disposition Price",
        default=False,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    exchange_journal_id = fields.Many2one(
        string="Exchange Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    disposal_journal_id = fields.Many2one(
        string="Disposal Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    gain_journal_id = fields.Many2one(
        string="Gain Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    exchange_account_id = fields.Many2one(
        string="Exchange Account",
        comodel_name="account.account",
        ondelete="restrict",
    )
    gain_account_id = fields.Many2one(
        string="Gain Account",
        comodel_name="account.account",
        ondelete="restrict",
    )
    loss_account_id = fields.Many2one(
        string="Loss Account",
        comodel_name="account.account",
        ondelete="restrict",
    )
    asset_retirement_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Asset Retirement",
        comodel_name="res.groups",
        relation="rel_type_asset_retirement_allowed_confirm_groups",
        column1="type_id",
        column2="group_id",
    )
    asset_retirement_open_grp_ids = fields.Many2many(
        string="Allowed To Open Asset Retirement",
        comodel_name="res.groups",
        relation="rel_type_asset_retirement_allowed_open_groups",
        column1="type_id",
        column2="group_id",
    )
    asset_retirement_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Asset Retirement",
        comodel_name="res.groups",
        relation="rel_type_asset_retirement_allowed_valid_groups",
        column1="type_id",
        column2="group_id",
    )
    asset_retirement_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Asset Retirement",
        comodel_name="res.groups",
        relation="rel_type_asset_retirement_allowed_cancel_groups",
        column1="type_id",
        column2="group_id",
    )
    asset_retirement_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Asset Retirement",
        comodel_name="res.groups",
        relation="rel_type_asset_retirement_allowed_restart_groups",
        column1="type_id",
        column2="group_id",
    )

# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    complex_asset_installation_sequence_id = fields.Many2one(
        string="Complex Asset Installation Sequence",
        comodel_name="ir.sequence",
    )
    complex_asset_installation_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Complex Asset Installation",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_installation_" "allowed_confirm_groups",
        column1="company_id",
        column2="group_id",
    )
    complex_asset_installation_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Complex Asset Installation",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_installation_allowed_valid_groups",
        column1="company_id",
        column2="group_id",
    )
    complex_asset_installation_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Complex Asset Installation",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_installation_" "allowed_cancel_groups",
        column1="company_id",
        column2="group_id",
    )
    complex_asset_installation_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Complex Asset Installation",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_installation_" "allowed_restart_groups",
        column1="company_id",
        column2="group_id",
    )
    complex_asset_removal_sequence_id = fields.Many2one(
        string="Complex Asset Removal Sequence",
        comodel_name="ir.sequence",
    )
    complex_asset_removal_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Complex Asset Removal",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_removal_allowed_confirm_groups",
        column1="company_id",
        column2="group_id",
    )
    complex_asset_removal_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Complex Asset Removal",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_removal_allowed_valid_groups",
        column1="company_id",
        column2="group_id",
    )
    complex_asset_removal_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Complex Asset Removal",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_removal_allowed_cancel_groups",
        column1="company_id",
        column2="group_id",
    )
    complex_asset_removal_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Complex Asset Removal",
        comodel_name="res.groups",
        relation="rel_company_complex_asset_removal_allowed_restart_groups",
        column1="company_id",
        column2="group_id",
    )

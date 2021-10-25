# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    asset_improvement_sequence_id = fields.Many2one(
        string="Fixed Asset Improvement Sequence",
        comodel_name="ir.sequence",
    )
    asset_improvement_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Fixed Asset Improvement",
        comodel_name="res.groups",
        relation="rel_company_asset_improvement_allowed_confirm",
        column1="company_id",
        column2="group_id",
    )
    asset_improvement_open_grp_ids = fields.Many2many(
        string="Allowed To Start Fixed Asset Improvement",
        comodel_name="res.groups",
        relation="rel_company_asset_improvement_allowed_open",
        column1="company_id",
        column2="group_id",
    )
    asset_improvement_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Fixed Asset Improvement",
        comodel_name="res.groups",
        relation="rel_company_asset_improvement_allowed_valid",
        column1="company_id",
        column2="group_id",
    )
    asset_improvement_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Fixed Asset Improvement",
        comodel_name="res.groups",
        relation="rel_company_asset_improvement_allowed_cancel",
        column1="company_id",
        column2="group_id",
    )
    asset_improvement_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Fixed Asset Improvement",
        comodel_name="res.groups",
        relation="rel_company_asset_improvement_allowed_restart",
        column1="company_id",
        column2="group_id",
    )

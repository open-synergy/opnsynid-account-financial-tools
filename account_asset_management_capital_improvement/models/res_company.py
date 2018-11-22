# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


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

    @api.model
    def _get_asset_improvement_button_policy_map(self):
        return [
            ("confirm_ok",
                "asset_improvement_confirm_grp_ids"),
            ("valid_ok", "asset_improvement_valid_grp_ids"),
            ("open_ok", "asset_improvement_open_grp_ids"),
            ("cancel_ok", "asset_improvement_cancel_grp_ids"),
            ("restart_ok", "asset_improvement_restart_grp_ids"),
        ]

    @api.multi
    def _get_asset_improvement_button_policy(self, policy_field):
        self.ensure_one()
        result = False
        button_group_ids = []
        user = self.env.user
        group_ids = user.groups_id.ids

        button_group_ids += getattr(
            self, policy_field).ids

        if not button_group_ids:
            result = True
        else:
            if (set(button_group_ids) & set(group_ids)):
                result = True
        return result

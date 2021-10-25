# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResConfig(models.TransientModel):
    _inherit = "account.asset.config_setting"

    asset_improvement_sequence_id = fields.Many2one(
        string="Fixed Asset Improvement Sequence",
        comodel_name="ir.sequence",
        related="company_id.asset_improvement_sequence_id",
        store=False,
    )
    asset_improvement_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Fixed Asset Improvement",
        comodel_name="res.groups",
        related="company_id.asset_improvement_confirm_grp_ids",
        store=False,
    )
    asset_improvement_open_grp_ids = fields.Many2many(
        string="Allowed To Start Fixed Asset Improvement",
        comodel_name="res.groups",
        related="company_id.asset_improvement_open_grp_ids",
        store=False,
    )
    asset_improvement_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Fixed Asset Improvement",
        comodel_name="res.groups",
        related="company_id.asset_improvement_valid_grp_ids",
        store=False,
    )
    asset_improvement_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Fixed Asset Improvement",
        comodel_name="res.groups",
        related="company_id.asset_improvement_cancel_grp_ids",
        store=False,
    )
    asset_improvement_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Fixed Asset Improvement",
        comodel_name="res.groups",
        related="company_id.asset_improvement_restart_grp_ids",
        store=False,
    )

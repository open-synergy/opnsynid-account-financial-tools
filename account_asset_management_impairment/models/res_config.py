# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResConfig(models.TransientModel):
    _inherit = "account.asset.config_setting"

    fixed_asset_impairment_sequence_id = fields.Many2one(
        string="Fixed Asset Impairment Sequence",
        comodel_name="ir.sequence",
        related="company_id.fixed_asset_impairment_sequence_id",
        store=False,
    )
    fixed_asset_impairment_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Fixed Asset Impairment",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_confirm_grp_ids",
        store=False,
    )
    fixed_asset_impairment_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Fixed Asset Impairment",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_valid_grp_ids",
        store=False,
    )
    fixed_asset_impairment_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Fixed Asset Impairment",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_cancel_grp_ids",
        store=False,
    )
    fixed_asset_impairment_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Fixed Asset Impairment",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_restart_grp_ids",
        store=False,
    )
    fixed_asset_impairment_reversal_sequence_id = fields.Many2one(
        string="Fixed Asset Impairment Reversal Sequence",
        comodel_name="ir.sequence",
        related="company_id.fixed_asset_impairment_reversal_sequence_id",
        store=False,
    )
    fixed_asset_impairment_reversal_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Fixed Asset Impairment Reversal",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_reversal_confirm_grp_ids",
        store=False,
    )
    fixed_asset_impairment_reversal_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Fixed Asset Impairment Reversal",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_reversal_valid_grp_ids",
        store=False,
    )
    fixed_asset_impairment_reversal_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Fixed Asset Impairment Reversal",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_reversal_cancel_grp_ids",
        store=False,
    )
    fixed_asset_impairment_reversal_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Fixed Asset Impairment Reversal",
        comodel_name="res.groups",
        related="company_id.fixed_asset_impairment_reversal_restart_grp_ids",
        store=False,
    )

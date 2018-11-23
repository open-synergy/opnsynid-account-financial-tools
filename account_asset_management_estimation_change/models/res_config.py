# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResConfig(models.TransientModel):
    _inherit = "account.asset.config_setting"

    asset_useful_life_sequence_id = fields.Many2one(
        string="Fixed Asset Useful Life Estimation Change Sequence",
        comodel_name="ir.sequence",
        related="company_id.asset_useful_life_sequence_id",
        store=False,
    )
    asset_useful_life_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Fixed Asset Useful Life Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_useful_life_confirm_grp_ids",
        store=False,
    )
    asset_useful_life_open_grp_ids = fields.Many2many(
        string="Allowed To Start Fixed Asset Useful Life Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_useful_life_open_grp_ids",
        store=False,
    )
    asset_useful_life_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Fixed Asset Useful Life Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_useful_life_valid_grp_ids",
        store=False,
    )
    asset_useful_life_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Fixed Asset Useful Life Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_useful_life_cancel_grp_ids",
        store=False,
    )
    asset_useful_life_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Fixed Asset Useful Life Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_useful_life_restart_grp_ids",
        store=False,
    )
    asset_salvage_sequence_id = fields.Many2one(
        string="Fixed Asset Salvage Value Estimation Change Sequence",
        comodel_name="ir.sequence",
        related="company_id.asset_salvage_sequence_id",
        store=False,
    )
    asset_salvage_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Fixed Asset Salvage Value "
               "Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_salvage_confirm_grp_ids",
        store=False,
    )
    asset_salvage_open_grp_ids = fields.Many2many(
        string="Allowed To Start Fixed Asset Salvage Value Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_salvage_open_grp_ids",
        store=False,
    )
    asset_salvage_valid_grp_ids = fields.Many2many(
        string="Allowed To Validate Fixed Asset Salvage Value "
               "Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_salvage_valid_grp_ids",
        store=False,
    )
    asset_salvage_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Fixed Asset Salvage Value Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_salvage_cancel_grp_ids",
        store=False,
    )
    asset_salvage_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Fixed Asset Salvage Value "
               "Estimation Change",
        comodel_name="res.groups",
        related="company_id.asset_salvage_restart_grp_ids",
        store=False,
    )

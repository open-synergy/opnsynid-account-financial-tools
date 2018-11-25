# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResConfig(models.TransientModel):
    _inherit = "account.asset.config_setting"

    auto_capitalization_limit = fields.Float(
        string="Auto Capitalization Limit",
        related="company_id.auto_capitalization_limit",
        store=False,
    )

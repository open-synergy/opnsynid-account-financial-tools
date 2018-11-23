# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountAssetDepreciationLine(models.Model):
    _inherit = "account.asset.depreciation.line"

    subtype_id = fields.Many2one(
        string="Subtype",
        comodel_name="account.asset_depreciation_line_subtype",
        ondelete="restrict",
    )

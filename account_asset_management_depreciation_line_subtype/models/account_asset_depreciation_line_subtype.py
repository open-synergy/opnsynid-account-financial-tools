# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountAssetDepreciationLineSubtype(models.Model):
    _name = "account.asset_depreciation_line_subtype"
    _description = "Depreciation Line Subtype"

    name = fields.Char(
        string="Depreciation Line Subtype",
        required=True,
    )

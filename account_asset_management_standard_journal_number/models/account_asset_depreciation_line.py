# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class AccountAssetDepreciationLine(models.Model):
    _inherit = "account.asset.depreciation.line"

    def _setup_move_data(
        self, depreciation_line, depreciation_date, period_id, context
    ):
        move_data = super(AccountAssetDepreciationLine, self)._setup_move_data(
            depreciation_line, depreciation_date, period_id, context
        )
        move_data["name"] = "/"
        return move_data

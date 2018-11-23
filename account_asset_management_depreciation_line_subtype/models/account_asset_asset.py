# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    @api.multi
    def _prepare_posted_lines_domain(self):
        _super = super(AccountAsset, self)
        result = _super._prepare_posted_lines_domain()
        result.insert(0, "&")
        result.append(("subtype_id", "=", False))
        return result

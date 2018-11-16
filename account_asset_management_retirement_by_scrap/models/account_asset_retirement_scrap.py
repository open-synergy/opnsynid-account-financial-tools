# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class FixedAssetRetirementScrap(models.Model):
    _name = "account.asset_retirement_scrap"
    _inherit = ["account.asset_retirement_common"]
    _description = "Fixed Asset Retirement by Scrap"
    _table = "account_asset_retirement"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "account_asset_management_retirement_by_scrap."
            "retirement_type_scrap").id

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        type_id = self.env.ref(
            "account_asset_management_retirement_by_scrap."
            "retirement_type_scrap", False) and self.env.ref(
                "account_asset_management_retirement_by_scrap."
                "retirement_type_scrap") or self.env["account."
                                                     "asset_retirement_type"]
        args.append(("type_id", "=", type_id.id))
        return super(FixedAssetRetirementScrap, self).search(
            args=args, offset=offset, limit=limit,
            order=order, count=count)

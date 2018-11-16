# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class FixedAssetRetirementDonation(models.Model):
    _name = "account.asset_retirement_donation"
    _inherit = ["account.asset_retirement_common"]
    _description = "Fixed Asset Retirement by Donation"
    _table = "account_asset_retirement"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "account_asset_management_retirement_by_donation."
            "retirement_type_donation").id

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        asset_retirement_type =\
            self.env["account.asset_retirement_type"]
        type_id = self.env.ref(
            "account_asset_management_retirement_by_donation."
            "retirement_type_donation", False) and self.env.ref(
                "account_asset_management_retirement_by_donation."
                "retirement_type_donation") or asset_retirement_type
        args.append(("type_id", "=", type_id.id))
        return super(FixedAssetRetirementDonation, self).search(
            args=args, offset=offset, limit=limit,
            order=order, count=count)

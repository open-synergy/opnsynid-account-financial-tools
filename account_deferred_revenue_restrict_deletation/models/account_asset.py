# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class AccountAssetAsset(models.Model):
    _name = "account.asset.asset"
    _inherit = [
        "account.asset.asset",
    ]

    @api.constrains("active")
    def constrains_no_disable(self):
        for record in self:
            if not record.active:
                record._check_reverse()

    @api.multi
    def _check_reverse(self):
        self.ensure_one()
        for line in self.depreciation_line_ids:
            if not line.move_id:
                continue

            if line.move_id.reversal_id:
                continue

            error_message = _(
                """
            Context: Deferred revenue deletation
            Database ID: %s
            Problem: Journal entry are not reversed
            Solution: Reverse journal entry
            """
                % (self.id)
            )
            raise UserError(error_message)

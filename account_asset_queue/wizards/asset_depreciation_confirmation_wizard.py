# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AssetDepreciationConfirmationWizard(models.TransientModel):
    _name = "asset.depreciation.confirmation.wizard"
    _inherit = "asset.depreciation.confirmation.wizard"
    _description = "asset.depreciation.confirmation.wizard"

    @api.multi
    def asset_compute_queue(self):
        self.ensure_one()
        context = self._context
        self.env["account.asset.asset"].compute_generated_entries_queue(
            self.date, asset_type=context.get("asset_type")
        )

# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, models

from odoo.addons.queue_job.job import job


class AccountAssetAsset(models.Model):
    _name = "account.asset.asset"
    _inherit = "account.asset.asset"

    @api.model
    def compute_generated_entries_queue(self, date, asset_type=None):
        # Entries generated : one by grouped category and one by asset from ungrouped category
        type_domain = []
        if asset_type:
            type_domain = [("type", "=", asset_type)]

        ungrouped_assets = self.env["account.asset.asset"].search(
            type_domain
            + [("state", "=", "open"), ("category_id.group_entries", "=", False)]
        )
        ungrouped_assets._compute_entries_queue(date, group_entries=False)

        for grouped_category in self.env["account.asset.category"].search(
            type_domain + [("group_entries", "=", True)]
        ):
            assets = self.env["account.asset.asset"].search(
                [("state", "=", "open"), ("category_id", "=", grouped_category.id)]
            )
            assets._compute_entries_queue(date, group_entries=True)

    @api.multi
    def _compute_entries_queue(self, date, group_entries=False):
        depreciation_ids = self.env["account.asset.depreciation.line"].search(
            [
                ("asset_id", "in", self.ids),
                ("depreciation_date", "<=", date),
                ("move_check", "=", False),
            ]
        )
        if group_entries:
            depreciation_ids.create_grouped_move_queue()
            return True

        depreciation_ids.create_move_queue()


class AccountAssetDepreciationLine(models.Model):
    _name = "account.asset.depreciation.line"
    _inherit = "account.asset.depreciation.line"

    @api.multi
    @job
    def create_move(self, post_move=True):
        _super = super(AccountAssetDepreciationLine, self)
        return _super.create_move()

    @api.multi
    def create_move_queue(self, post_move=True):
        for record in self:
            description = (
                "Asset/Deferred Revenue Journal Entry Generation ID {} {}".format(
                    record.asset_id.id,
                    record.depreciation_date,
                )
            )
            record.with_context().with_delay(description=_(description)).create_move()

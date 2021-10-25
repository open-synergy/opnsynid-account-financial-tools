# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ComplexAssetRemoval(models.Model):
    _name = "account.complex_asset_removal"
    _description = "Complex Asset Removal"
    _inherit = "account.complex_asset_movement_common"
    _table = "account_complex_asset_movement"

    parent_asset_id = fields.Many2one(
        string="Remove Asset From",
    )

    @api.model
    def _default_movement_type(self):
        return "remove"

    @api.onchange("asset_id")
    def onchange_parent_id(self):
        self.parent_asset_id = self.asset_id.parent_id

    @api.multi
    def action_valid(self):
        _super = super(ComplexAssetRemoval, self)
        _super.action_valid()
        for rec in self:
            rec.asset_id.write(
                {
                    "parent_id": False,
                }
            )

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args.append(("movement_type", "=", "remove"))
        return super(ComplexAssetRemoval, self).search(
            args=args, offset=offset, limit=limit, order=order, count=count
        )

# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAsset(models.Model):
    _inherit = "account.asset.asset"

    @api.multi
    @api.depends("improvement_ids", "improvement_ids.state")
    def _compute_improvement(self):
        for asset in self:
            improvement = 0.0
            for imp in asset.improvement_ids.filtered(lambda r: r.state == "valid"):
                improvement += imp.improvement_amount
            asset.amount_improvement = improvement

    @api.multi
    @api.depends(
        "asset_value",
        "amount_improvement",
        "depreciation_line_ids",
        "depreciation_line_ids.amount",
        "depreciation_line_ids.previous_id",
        "depreciation_line_ids.init_entry",
        "depreciation_line_ids.move_id",
    )
    def _compute_depreciation(self):
        _super = super(AccountAsset, self)
        _super._compute_depreciation()

    @api.multi
    @api.depends(
        "purchase_value", "amount_improvement", "salvage_value", "type", "method"
    )
    def _asset_value(self):
        _super = super(AccountAsset, self)
        _super._asset_value()

    improvement_ids = fields.One2many(
        string="Improvement",
        comodel_name="account.asset_improvement",
        inverse_name="asset_id",
        readonly=True,
    )
    amount_improvement = fields.Float(
        string="Improvement Value",
        compute="_compute_improvement",
        store=True,
    )
    value_residual = fields.Float(
        compute="_compute_depreciation",
    )
    value_depreciated = fields.Float(
        compute="_compute_depreciation",
    )
    asset_value = fields.Float(
        compute="_asset_value",  # pylint: disable=C8108
    )

    @api.model
    def _get_asset_value_field(self):
        _super = super(AccountAsset, self)
        result = _super._get_asset_value_field()
        result += [("+", "amount_improvement")]
        return result

    @api.model
    def _get_additional_depreciated_value_field(self):
        _super = super(AccountAsset, self)
        result = _super._get_additional_depreciated_value_field()
        result += [("+", "amount_improvement")]
        return result

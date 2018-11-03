# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ComplexAssetInstallation(models.Model):
    _name = "account.complex_asset_installation"
    _inherit = "account.complex_asset_movement_common"
    _table = "account_complex_asset_movement"

    parent_asset_id = fields.Many2one(
        string="Install Asset On",
    )

    @api.multi
    def action_valid(self):
        _super = super(ComplexAssetInstallation, self)
        _super.action_valid()
        for rec in self:
            rec.asset_id.write({
                "parent_id": rec.parent_asset_id.id,
            })

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args.append(("movement_type", "=", "add"))
        return super(ComplexAssetInstallation, self).search(
            args=args, offset=offset, limit=limit,
            order=order, count=count)

    @api.multi
    def _get_sequence(self):
        self.ensure_one()
        company = self.company_id
        if company.complex_asset_installation_sequence_id:
            result = company.complex_asset_installation_sequence_id
        else:
            result = self.env.ref(
                "account_asset_management_complex_asset.sequence_"
                "complex_asset_installation")
        return result

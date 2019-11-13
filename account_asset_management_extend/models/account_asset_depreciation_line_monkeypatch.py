# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from openerp.addons.account_asset_management.\
    account_asset import account_asset_depreciation_line
from openerp.exceptions import Warning as UserError


@api.multi
def write(self, vals):
    for dl in self:
        if vals.keys() == ['move_id'] and not vals['move_id']:
            # allow to remove an accounting entry via the
            # 'Delete Move' button on the depreciation lines.
            if not self.env.context.get('unlink_from_asset'):
                raise UserError(
                    _("You are not allowed to remove an accounting entry "
                      "linked to an asset."
                      "\nYou should remove such entries from the asset."))
        elif vals.keys() == ['asset_id']:
            continue
        elif dl.move_id and \
                not self.env.context.get('allow_asset_line_update'):
            raise UserError(
                _("You cannot change a depreciation line "
                  "with an associated accounting entry."))
        elif vals.get('init_entry'):
            self.env.cr.execute(
                "SELECT id "
                "FROM account_asset_depreciation_line "
                "WHERE asset_id = %s AND move_check = TRUE "
                "AND type = 'depreciate' AND line_date <= %s LIMIT 1",
                (dl.asset_id.id, dl.line_date))
            res = self.env.cr.fetchone()
            if res:
                raise UserError(
                    _("You cannot set the 'Initial Balance Entry' flag "
                      "on a depreciation line "
                      "with prior posted entries."))
    return super(account_asset_depreciation_line, self).write(vals)


class AccountAssetDepreciationLineMonkeypatch(models.TransientModel):
    _name = "account.asset.depreciation.line.monkeypatch"
    _description = "Asset Depreciation Line Monkeypatch"

    def _register_hook(self, cr):
        account_asset_depreciation_line.write = \
            write
        _super = super(AccountAssetDepreciationLineMonkeypatch, self)
        return _super._register_hook(cr)

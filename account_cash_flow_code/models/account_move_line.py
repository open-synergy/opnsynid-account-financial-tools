# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    direct_cash_flow_id = fields.Many2one(
        string="Direct Cash Flow",
        comodel_name="account.cash_flow_code",
        domain=[
            ("type", "=", "direct"),
        ],
    )
    indirect_cash_flow_id = fields.Many2one(
        string="Indirect Cash Flow",
        comodel_name="account.cash_flow_code",
        domain=[
            ("type", "=", "indirect"),
        ],
    )

    def onchange_account_id(
        self, cr, uid, ids, account_id=False, partner_id=False, context=None
    ):
        res = super(AccountMoveLine, self).onchange_account_id(
            cr, uid, ids, account_id, partner_id, context
        )
        if account_id:
            direct_cf = (
                self.pool["account.account"]
                .browse(cr, uid, account_id)
                .direct_cash_flow_id
            )
            indirect_cf = (
                self.pool["account.account"]
                .browse(cr, uid, account_id)
                .indirect_cash_flow_id
            )
            if direct_cf:
                vals = {"direct_cash_flow_id": direct_cf.id}
                res["value"].update(vals)
            else:
                vals = {"direct_cash_flow_id": False}
                res["value"].update(vals)
            if indirect_cf:
                vals = {"indirect_cash_flow_id": indirect_cf.id}
                res["value"].update(vals)
            else:
                vals = {"indirect_cash_flow_id": False}
                res["value"].update(vals)
        return res

    @api.onchange("account_id")
    def onchange_account_direct_indirect_id(self):
        account = self.account_id
        if account:
            if account.direct_cash_flow_id:
                self.direct_cash_flow_id = account.direct_cash_flow_id.id
            else:
                self.direct_cash_flow_id = False
            if account.indirect_cash_flow_id:
                self.indirect_cash_flow_id = account.indirect_cash_flow_id.id
            else:
                self.indirect_cash_flow_id = False

    @api.model
    def create(self, vals):
        obj_account = self.env["account.account"]
        account_id = vals["account_id"]
        if account_id:
            account = obj_account.browse(account_id)
            if account.direct_cash_flow_id and not vals.get(
                "direct_cash_flow_id", False
            ):
                vals["direct_cash_flow_id"] = account.direct_cash_flow_id.id
            if account.indirect_cash_flow_id and not vals.get(
                "indirect_cash_flow_id", False
            ):
                vals["indirect_cash_flow_id"] = account.indirect_cash_flow_id.id
        return super(AccountMoveLine, self).create(vals)

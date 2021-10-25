# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.

from openerp import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

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

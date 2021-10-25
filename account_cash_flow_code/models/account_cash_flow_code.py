# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountCashFlowCode(models.Model):
    _name = "account.cash_flow_code"
    _description = "Cash Flow Code"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
    type = fields.Selection(
        string="Type",
        selection=[("direct", "Direct"), ("indirect", "Indirect")],
        required=True,
    )

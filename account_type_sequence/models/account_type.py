# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountType(models.Model):
    _inherit = "account.account.type"
    _order = "sequence, name"

    sequence = fields.Integer(
        string="Sequence"
    )

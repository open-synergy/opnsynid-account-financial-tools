# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountPaymentTermn(models.Model):
    _inherit = "account.payment.term"

    accurate_termsid = fields.Char(
        string='Accurate TERMSID'
        )

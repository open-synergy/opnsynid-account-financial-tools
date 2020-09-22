# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = [
        "account.move",
        "mail.thread"
    ]

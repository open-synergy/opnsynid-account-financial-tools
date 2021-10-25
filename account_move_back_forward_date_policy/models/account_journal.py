# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    allow_back_date = fields.Boolean(
        string="Allow Back Date",
        default=True,
    )

    allow_forward_date = fields.Boolean(
        string="Allow Forward Date",
        default=True,
    )

# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    subtype_id = fields.Many2one(
        string="Subtype",
        comodel_name="account.journal_subtype",
    )

    @api.onchange("type")
    def onchange_type(self):
        self.subtype_id = False

# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    allowed_group_bank_ids = fields.Many2many(
        string='Allowed Group Bank',
        comodel_name='res.groups',
        relation='journal_group_bank_rel',
        column1='journal_id',
        column2='group_id')

    allowed_group_cash_ids = fields.Many2many(
        string='Allowed Group Cash',
        comodel_name='res.groups',
        relation='journal_group_cash_rel',
        column1='journal_id',
        column2='group_id')

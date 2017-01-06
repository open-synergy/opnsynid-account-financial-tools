# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestBaseCreateMenu(TransactionCase):
    def setUp(self):
        super(TestBaseCreateMenu, self).setUp()
        # Object
        self.wiz =\
            self.env['account.journal_bank_cash_create_menu']
        self.obj_journal =\
            self.env['account.journal']

        # Data
        self.bank_journal =\
            self.env.ref('account.bank_journal')

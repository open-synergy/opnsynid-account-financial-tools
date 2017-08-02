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
        self.search_bank_view =\
            self.env.ref('account.view_bank_statement_search')
        self.tree_bank_view =\
            self.env.ref('account.view_bank_statement_tree')
        self.from_bank_view =\
            self.env.ref('account.view_bank_statement_form')
        self.parent_menu =\
            self.env.ref('account.account_account_menu')

    def _create_menu(self, parent_menu_id=False):
        new = self.wiz.with_context(
            active_model="account.journal",
            active_ids=[self.bank_journal.id]
        ).new()

        new.parent_menu_id = parent_menu_id
        new.menu_name = self.bank_journal.name
        new.search_view_id = self.search_bank_view.id
        new.view_ids = [
            (0, 0, {
                'sequence': 1,
                'view_id': self.tree_bank_view.id,
                'view_mode': 'tree'
                }),
            (0, 0, {
                'sequence': 2,
                'view_id': self.from_bank_view.id,
                'view_mode': 'form'
                })
        ]

        # Create Menu
        new.button_create_menu()
        return True

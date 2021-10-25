# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from openerp.tests.common import TransactionCase


class TestReconcilation(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestReconcilation, self).setUp(*args, **kwargs)
        # Objects
        self.obj_res_groups = self.env["res.groups"]
        self.obj_bank_stmt = self.env["account.bank.statement"]
        self.obj_bank_stmt_line = self.env["account.bank.statement.line"]
        self.obj_invoice = self.env["account.invoice"]
        self.obj_invoice_line = self.env["account.invoice.line"]

        # Data
        self.data_bnk_stmt = self.env.ref("account.demo_bank_statement_1")
        self.data_journal = self.env.ref("account.bank_journal")
        self.data_journal_cash = self.env.ref("account.cash_journal")
        self.data_journal_no_bankcash = self.env.ref("account.miscellaneous_journal")
        self.partner_1 = self.env.ref("base.res_partner_1")
        self.partner_2 = self.env.ref("base.res_partner_2")
        self.account = self.env.ref("account.a_recv")
        self.product_1 = self.env.ref("product.product_product_3")
        self.product_2 = self.env.ref("product.product_product_4")
        self.curr = self.env.ref("base.IDR")
        self.group = self._create_group()

    def _create_group(self):
        vals = {"name": "Group Allowed Import"}
        group = self.obj_res_groups.create(vals)
        return group

    def _create_invoice_cash(self):
        invoice_id = self.obj_invoice.create(
            {
                "partner_id": self.partner_1.id,
                "reference_type": "none",
                "currency_id": self.curr.id,
                "name": "invoice to client",
                "account_id": self.account.id,
                "type": "out_invoice",
                "date_invoice": time.strftime("%Y") + "-07-01",
            }
        )
        self.obj_invoice_line.create(
            {
                "product_id": self.product_1.id,
                "quantity": 1,
                "price_unit": 1000000,
                "invoice_id": invoice_id.id,
                "name": "Test 1",
            }
        )
        return invoice_id

    def _create_invoice_no_bankcash(self):
        invoice_id = self.obj_invoice.create(
            {
                "partner_id": self.partner_2.id,
                "reference_type": "none",
                "currency_id": self.curr.id,
                "name": "invoice to client",
                "account_id": self.account.id,
                "type": "out_invoice",
                "date_invoice": time.strftime("%Y") + "-07-01",
            }
        )
        self.obj_invoice_line.create(
            {
                "product_id": self.product_2.id,
                "quantity": 1,
                "price_unit": 50000000,
                "invoice_id": invoice_id.id,
                "name": "Test 2",
            }
        )
        return invoice_id

    def _create_bank_statement_cash(self):
        bank_stmt_id = self.obj_bank_stmt.create(
            {
                "journal_id": self.data_journal_cash.id,
                "date": time.strftime("%Y") + "-07-15",
            }
        )

        self.obj_bank_stmt_line.create(
            {
                "name": "half payment",
                "statement_id": bank_stmt_id.id,
                "partner_id": self.partner_1.id,
                "amount": 750000,
                "amount_currency": 750000,
                "currency_id": self.curr.id,
                "date": time.strftime("%Y") + "-07-15",
            }
        )
        return bank_stmt_id

    def _create_bank_statement_no_bankcash(self):
        bank_stmt_id = self.obj_bank_stmt.create(
            {
                "journal_id": self.data_journal_no_bankcash.id,
                "date": time.strftime("%Y") + "-07-15",
            }
        )

        self.obj_bank_stmt_line.create(
            {
                "name": "half payment",
                "statement_id": bank_stmt_id.id,
                "partner_id": self.partner_2.id,
                "amount": 12500000,
                "amount_currency": 12500000,
                "currency_id": self.curr.id,
                "date": time.strftime("%Y") + "-07-15",
            }
        )
        return bank_stmt_id

    def test_reconciliation_bank(self):
        # Test User No Group, Account Journal No Group
        for st_line in self.data_bnk_stmt.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertNotEqual(result, [])

        # Insert Group to Account Jounal
        self.data_journal.allowed_group_bank_ids = [(6, 0, self.group.ids)]

        # Test User No Group, Account Journal Has Group
        for st_line in self.data_bnk_stmt.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertEqual(result, [])

        # Test User Has Group, Account Journal Has Group
        user = self.env.user
        user.groups_id = [(6, 0, self.group.ids)]
        for st_line in self.data_bnk_stmt.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertNotEqual(result, [])

    def test_reconciliation_cash(self):
        # Create Invoice
        invoice = self._create_invoice_cash()
        invoice.signal_workflow("invoice_open")

        # Create Bank Statement Cash
        bank_stmt_id = self._create_bank_statement_cash()

        # Test User No Group, Account Journal No Group
        for st_line in bank_stmt_id.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertNotEqual(result, [])

        # Insert Group to Account Jounal
        self.data_journal_cash.allowed_group_cash_ids = [(6, 0, self.group.ids)]

        # Test User No Group, Account Journal Has Group
        for st_line in bank_stmt_id.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertEqual(result, [])

        # Test User Has Group, Account Journal Has Group
        user = self.env.user
        user.groups_id = [(6, 0, self.group.ids)]
        for st_line in bank_stmt_id.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertNotEqual(result, [])

    def test_reconciliation_no_bankcash(self):
        # Create Invoice
        invoice = self._create_invoice_no_bankcash()
        invoice.signal_workflow("invoice_open")

        # Create Bank Statement Cash
        bank_stmt_id = self._create_bank_statement_no_bankcash()

        # Test User No Group, Account Journal No Group
        for st_line in bank_stmt_id.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertNotEqual(result, [])

        # Insert Group to Account Jounal
        self.data_journal_no_bankcash.allowed_group_cash_ids = [(6, 0, self.group.ids)]

        # Test User No Group, Account Journal Has Group
        for st_line in bank_stmt_id.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertNotEqual(result, [])

        # Test User Has Group, Account Journal Has Group
        user = self.env.user
        user.groups_id = [(6, 0, self.group.ids)]
        for st_line in bank_stmt_id.line_ids:
            result = self.obj_bank_stmt_line.get_move_lines_for_reconciliation(
                st_line=st_line
            )
            self.assertNotEqual(result, [])

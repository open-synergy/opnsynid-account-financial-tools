# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from datetime import datetime


class TestComputeInvoicePolicy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputeInvoicePolicy, self).setUp(*args, **kwargs)
        # Objects
        self.obj_account_invoice = self.env['account.invoice']
        self.obj_account_invoice_line = self.env['account.invoice.line']
        self.obj_res_groups = self.env['res.groups']
        self.obj_res_users = self.env['res.users']

        # Data
        self.partner = self.env.ref('base.res_partner_3')
        self.curr = self.env.ref("base.IDR")
        self.account = self.env.ref('account.a_recv')
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.product =\
            self.env.ref('product.product_product_13')
        self.group_employee_id = self.ref('base.group_user')
        self.grp_po_manager =\
            self.env.ref(
                'account.group_account_manager')
        self.user_1 = self._create_user_1()
        self.user_2 = self._create_user_2()
        self.user_3 = self._create_user_3()

        # Add Group Button Validate
        self.grp_open = self.obj_res_groups.create({
            'name': 'Regular - Group Button Validate'
        })
        # Add Group Button Refund
        self.grp_refund = self.obj_res_groups.create({
            'name': 'Regular - Group Button Refund'
        })
        # Add Group Button Cancel
        self.grp_cancel = self.obj_res_groups.create({
            'name': 'Regular - Group Button Cancel'
        })
        # Add Group Button Set To Draft
        self.grp_set_to_draft = self.obj_res_groups.create({
            'name': 'Regular - Group Button Set To Draft'
        })
        # Add Group Button Re-Open
        self.grp_re_open = self.obj_res_groups.create({
            'name': 'Regular - Group Button Re-Open'
        })
        # Add Group Button Send by Email
        self.grp_send_email = self.obj_res_groups.create({
            'name': 'Regular - Group Button Send by Email'
        })
        # Add Group Button Proforma
        self.grp_proforma = self.obj_res_groups.create({
            'name': 'Regular - Group Button Proforma'
        })

    def _create_user_1(self):
        val = {
            'name': 'User Test 1',
            'login': 'user_1',
            'alias_name': 'user1',
            'email': 'user_test_1@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_po_manager.id
                ]
            )]
        }
        user_1 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_1

    def _create_user_2(self):
        val = {
            'name': 'User Test 2',
            'login': 'user_2',
            'alias_name': 'user2',
            'email': 'user_test_2@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_po_manager.id
                ]
            )]
        }
        user_2 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_2

    def _create_user_3(self):
        val = {
            'name': 'User Test 3',
            'login': 'user_3',
            'alias_name': 'user3',
            'email': 'user_test_3@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_po_manager.id
                ]
            )]
        }
        user_3 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_3

    def _create_invoice(self):
        vals = {
            'partner_id': self.partner.id,
            'reference_type': 'none',
            'currency_id': self.curr.id,
            'name': 'invoice to client',
            'account_id': self.account.id,
            'type': 'in_invoice',
            'date_invoice': self.date,
            'date_due': self.date
        }
        invoice_id = self.obj_account_invoice.create(vals)

        lines = {
            'product_id': self.product.id,
            'quantity': 1,
            'price_unit': 50000,
            'invoice_id': invoice_id.id,
            'name': 'Test Invoice'
        }
        self.obj_account_invoice_line.create(lines)

        return invoice_id

    def test_compute_case_admin(self):
        # Create Invoice
        invoice =\
            self._create_invoice()

        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, invoice.open_ok)
        self.assertEqual(True, invoice.refund_ok)
        self.assertEqual(True, invoice.cancel_ok)
        self.assertEqual(True, invoice.set_to_draft_ok)
        self.assertEqual(True, invoice.re_open_ok)
        self.assertEqual(True, invoice.send_email_ok)
        self.assertEqual(True, invoice.proforma_ok)

    def test_compute_case_1(self):
        # Create Invoice
        invoice =\
            self._create_invoice()

        # Condition :
        #   1. Log In As User 1
        #   2. Allowed to Validate has group
        #   3. Allowed to Refund has group
        #   4. Allowed to Cancel has group
        #   6. User 1 doesn't have group
        invoice.journal_id.open_group_ids = [(
            6, 0, [
                self.grp_open.id
            ]
        )]

        invoice.journal_id.refund_group_ids = [(
            6, 0, [
                self.grp_refund.id
            ]
        )]

        invoice.journal_id.cancel_group_ids = [(
            6, 0, [
                self.grp_cancel.id
            ]
        )]

        # Result
        #   1. User 1 cannot Validate
        #   2. User 1 cannot Refund
        #   3. User 1 cannot Cancel

        self.assertEqual(
            False,
            invoice.sudo(
                self.user_1.id).open_ok
        )
        self.assertEqual(
            False,
            invoice.sudo(
                self.user_1.id).refund_ok
        )
        self.assertEqual(
            False,
            invoice.sudo(
                self.user_1.id).cancel_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).set_to_draft_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).re_open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).send_email_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).proforma_ok
        )

        # Condition :
        #   1. User 1 have group
        # Add Group Validate
        self.user_1.groups_id = [(
            4,
            self.grp_open.id
        )]
        # Add Group Refund
        self.user_1.groups_id = [(
            4,
            self.grp_refund.id
        )]
        # Add Group Cancel
        self.user_1.groups_id = [(
            4,
            self.grp_cancel.id
        )]

        # Result
        #   1. User 1 can Validate
        #   2. User 1 can Refund
        #   3. User 1 can Cancel
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).refund_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).cancel_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).set_to_draft_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).re_open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).send_email_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_1.id).proforma_ok
        )

    def test_compute_case_2(self):
        # Create Invoice
        invoice =\
            self._create_invoice()

        # Condition :
        #   1. Log In As User 2
        #   2. Allowed to Set To Draft has group
        #   3. Allowed to Re-Open has group
        #   6. User 2 doesn't have group
        invoice.journal_id.set_to_draft_group_ids = [(
            6, 0, [
                self.grp_set_to_draft.id
            ]
        )]

        invoice.journal_id.re_open_group_ids = [(
            6, 0, [
                self.grp_re_open.id
            ]
        )]

        # Result
        #   1. User 2 cannot Set To Draft
        #   2. User 2 cannot Re-Open

        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).refund_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).cancel_ok
        )
        self.assertEqual(
            False,
            invoice.sudo(
                self.user_2.id).set_to_draft_ok
        )
        self.assertEqual(
            False,
            invoice.sudo(
                self.user_2.id).re_open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).send_email_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).proforma_ok
        )

        # Condition :
        #   1. User 2 have group
        # Add Group Set To Draft
        self.user_2.groups_id = [(
            4,
            self.grp_set_to_draft.id
        )]
        # Add Group Re-Open
        self.user_2.groups_id = [(
            4,
            self.grp_re_open.id
        )]

        # Result
        #   1. User 2 can Set To Draft
        #   2. User 2 can Re-Open
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).refund_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).cancel_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).set_to_draft_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).re_open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).send_email_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_2.id).proforma_ok
        )

    def test_compute_case_3(self):
        # Create Invoice
        invoice =\
            self._create_invoice()

        # Condition :
        #   1. Log In As User 3
        #   2. Allowed to Send by Email has group
        #   3. Allowed to PRO-FORMA has group
        #   6. User 3 doesn't have group
        invoice.journal_id.send_email_group_ids = [(
            6, 0, [
                self.grp_send_email.id
            ]
        )]

        invoice.journal_id.proforma_group_ids = [(
            6, 0, [
                self.grp_proforma.id
            ]
        )]

        # Result
        #   1. User 3 cannot Send by Email
        #   2. User 3 cannot PRO-FORMA

        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).refund_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).cancel_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).set_to_draft_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).re_open_ok
        )
        self.assertEqual(
            False,
            invoice.sudo(
                self.user_3.id).send_email_ok
        )
        self.assertEqual(
            False,
            invoice.sudo(
                self.user_3.id).proforma_ok
        )

        # Condition :
        #   1. User 3 have group
        # Add Group Send by Email
        self.user_3.groups_id = [(
            4,
            self.grp_send_email.id
        )]
        # Add Group PRO-FORMA
        self.user_3.groups_id = [(
            4,
            self.grp_proforma.id
        )]

        # Result
        #   1. User 3 can Send by Email
        #   2. User 3 can PRO-FORMA
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).refund_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).cancel_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).set_to_draft_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).re_open_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).send_email_ok
        )
        self.assertEqual(
            True,
            invoice.sudo(
                self.user_3.id).proforma_ok
        )

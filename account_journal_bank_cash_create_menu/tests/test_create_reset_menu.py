# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBaseCreateMenu


class TestCreateResetMenu(TestBaseCreateMenu):
    def test_create_reset_menu(self):
        new = self.wiz.with_context(
            active_model="account.journal",
            active_ids=[self.bank_journal.id]
        ).new()

        new.menu_name = self.bank_journal.name
        # Create Menu
        new.button_create_menu()

        # Check menu_id & window_action_id
        # Condition : menu_id or window_action_id == False
        result_menu_id = False
        result_window_action_id = False

        if self.bank_journal.menu_id.id:
            result_menu_id = True
        self.assertEqual(
            True,
            result_menu_id
        )
        if self.bank_journal.window_action_id.id:
            result_window_action_id = True
        self.assertEqual(
            True,
            result_window_action_id
        )

        # Pressing Reset Button
        self.bank_journal.button_reset_menu()

        # Check menu_id & window_action_id
        # Condition : menu_id or window_action_id == False
        self.assertEqual(
            False,
            self.bank_journal.menu_id.id
        )
        self.assertEqual(
            False,
            self.bank_journal.window_action_id.id
        )

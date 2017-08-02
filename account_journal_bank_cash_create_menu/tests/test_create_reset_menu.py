# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBaseCreateMenu


class TestCreateResetMenu(TestBaseCreateMenu):
    def test_create_menu(self):
        self._create_menu()

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

    def test_create_menu_2(self):
        self._create_menu()

        # Check menu_id & window_action_id
        # Condition : menu_id or window_action_id == False
        result_menu_id = False
        result_window_action_id = False

        if self.bank_journal.menu_id.id:
            result_menu_id = True
            menu_id = self.bank_journal.menu_id.id
        self.assertEqual(
            True,
            result_menu_id
        )
        if self.bank_journal.window_action_id.id:
            result_window_action_id = True
            waction_id =\
                self.bank_journal.window_action_id.id
        self.assertEqual(
            True,
            result_window_action_id
        )

        # Check menu_id & window_action_id
        # Condition : menu_id or window_action_id == True
        self._create_menu()

        self.assertEqual(
            self.bank_journal.menu_id.id,
            menu_id
        )
        self.assertEqual(
            self.bank_journal.window_action_id.id,
            waction_id
        )

    def test_create_menu_3(self):
        # Create Menu With Parent Menu ID

        self._create_menu(self.parent_menu.id)

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

    def test_reset_menu(self):
        self._create_menu()

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

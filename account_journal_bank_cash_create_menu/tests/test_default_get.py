# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBaseCreateMenu


class TestDefaultGet(TestBaseCreateMenu):
    def test_default_get(self):
        default = self.wiz.with_context(
            active_model="account.journal",
            active_ids=[self.bank_journal.id]
        ).default_get({})

        # Check Default Menu Name
        self.assertEqual(
            default['menu_name'],
            self.bank_journal.name
        )

        # Check Default Sequence
        self.assertEqual(
            default['sequence'],
            1
        )

# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    @api.multi
    def _check_group(self):
        self.ensure_one()
        groups_id = []
        user = self.env.user

        if self.journal_id.type == 'cash':
            if self.journal_id.allowed_group_cash_ids:
                groups_id = self.journal_id.allowed_group_cash_ids.ids
        elif self.journal_id.type == 'bank':
            if self.journal_id.allowed_group_bank_ids:
                groups_id = self.journal_id.allowed_group_bank_ids.ids
        else:
            return True

        if groups_id:
            if frozenset(user.groups_id.ids).intersection(groups_id):
                return True
            else:
                return False
        else:
            return True

    @api.multi
    def get_move_lines_for_reconciliation_widget(
        self, excluded_ids=None, str=False,
        offset=0, limit=None
    ):
        res = super(
            AccountBankStatementLine, self
        ).get_move_lines_for_reconciliation_widget(
            excluded_ids=None, str=False,
            offset=0, limit=None
        )
        if self._check_group():
            return res
        else:
            return []

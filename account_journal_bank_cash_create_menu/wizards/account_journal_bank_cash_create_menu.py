# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountJournalBankCashCreateMenu(models.TransientModel):
    _name = "account.journal_bank_cash_create_menu"
    _description = "Account Journal Bank Cash Create Menu"

    menu_name = fields.Char(
        string="Menu Name",
        required=True
    )

    parent_menu_id = fields.Many2one(
        string="Parent Menu",
        comodel_name="ir.ui.menu"
    )

    sequence = fields.Integer(
        string="Sequence"
    )

    search_view_id = fields.Many2one(
        string="Search View Ref",
        comodel_name="ir.ui.view"
    )

    view_ids = fields.One2many(
        string="Views",
        comodel_name="account.journal_bank_cash_create_menu_view_detail",
        inverse_name="wizard_id"
    )

    @api.model
    def default_get(self, fields):
        res = super(AccountJournalBankCashCreateMenu, self).default_get(
            fields)
        obj_journal = self.env['account.journal']
        journal_ids = self.env.context['active_ids']

        journal = obj_journal.browse(journal_ids)
        res['menu_name'] = journal.name
        res['sequence'] = 1
        return res

    @api.model
    def _create_window_action(self, journal):
        obj_act_window = self.env['ir.actions.act_window']
        obj_act_window_view =\
            self.env['ir.actions.act_window.view']

        if not journal.window_action_id:
            res = {
                "name": journal.display_name,
                "type": "ir.actions.act_window",
                "domain": [('journal_id', '=', journal.id)],
                "context": {
                    'default_journal_id': journal.id
                },
                "search_view_id": self.search_view_id and
                self.search_view_id.id or False,
                "res_model": 'account.bank.statement',
                "view_type": 'form',
                "view_mode": 'tree,form',
            }

            window_action_id = obj_act_window.create(res)
            journal.window_action_id = window_action_id.id

            if self.view_ids:
                for view in self.view_ids:
                    res_view = {
                        'sequence': view.sequence,
                        'view_id': view.view_id.id,
                        'view_mode': view.view_mode,
                        'act_window_id': window_action_id.id
                    }
                    obj_act_window_view.create(res_view)

            return window_action_id
        return False

    @api.model
    def _create_menu(self, journal, window_action):
        obj_ir_ui_menu = self.env['ir.ui.menu']
        bankandcash_menu = self.env.ref('account.menu_finance_bank_and_cash')

        if not self.parent_menu_id:
            parent_id = bankandcash_menu.id
        else:
            parent_id = self.parent_menu_id.id

        if not journal.menu_id:
            res = {
                'name': self.menu_name,
                'sequence': self.sequence,
                'parent_id': parent_id,
                'action': 'ir.actions.act_window,%s' % window_action.id
            }

            menu_id = obj_ir_ui_menu.create(res)
            journal.menu_id = menu_id.id

            return menu_id
        return False

    @api.multi
    def button_create_menu(self):
        self.ensure_one()

        obj_journal = self.env['account.journal']
        journal_ids = self.env.context['active_ids']

        journal = obj_journal.browse(journal_ids)

        window_action_id =\
            self._create_window_action(journal)

        self._create_menu(
            journal, window_action_id)


VIEW_TYPES = [
    ('tree', 'Tree'),
    ('form', 'Form'),
    ('graph', 'Graph'),
    ('calendar', 'Calendar'),
    ('gantt', 'Gantt'),
    ('kanban', 'Kanban')]


class AccountJournalBankCashCreateMenuViewDetail(models.TransientModel):
    _name = "account.journal_bank_cash_create_menu_view_detail"
    _description = "Account Journal Bank Cash Create Menu View Detail"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="account.journal_bank_cash_create_menu"
    )

    sequence = fields.Integer(
        string="Sequence"
    )

    view_id = fields.Many2one(
        string="Views",
        comodel_name="ir.ui.view"
    )

    view_mode = fields.Selection(
        string="View Type",
        required=True,
        selection=VIEW_TYPES
    )

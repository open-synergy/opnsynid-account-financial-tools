# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    # Bank Statement
    bank_stmt_reconcile_group_ids = fields.Many2many(
        string="Allowed to Reconcile",
        comodel_name="res.groups",
        relation="rel_bank_stmt_reconcile_groups",
        column1="journal_id",
        column2="group_id",
    )

    bank_stmt_close_group_ids = fields.Many2many(
        string="Allowed to Close",
        comodel_name="res.groups",
        relation="rel_bank_stmt_close_groups",
        column1="journal_id",
        column2="group_id",
    )

    bank_stmt_cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        relation="rel_bank_stmt_cancel_groups",
        column1="journal_id",
        column2="group_id",
    )

    # Cash Register
    cash_register_reconcile_group_ids = fields.Many2many(
        string="Allowed to Reconcile",
        comodel_name="res.groups",
        relation="rel_cash_register_reconcile_groups",
        column1="journal_id",
        column2="group_id",
    )
    cash_register_close_group_ids = fields.Many2many(
        string="Allowed to Close CashBox",
        comodel_name="res.groups",
        relation="rel_cash_register_close_groups",
        column1="journal_id",
        column2="group_id",
    )
    cash_register_open_group_ids = fields.Many2many(
        string="Allowed to Open CashBox",
        comodel_name="res.groups",
        relation="rel_cash_register_open_groups",
        column1="journal_id",
        column2="group_id",
    )
    cash_register_cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        relation="rel_cash_register_cancel_groups",
        column1="journal_id",
        column2="group_id",
    )

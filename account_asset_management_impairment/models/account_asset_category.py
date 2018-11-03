# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountAssetCategory(models.Model):
    _inherit = "account.asset.category"

    impairment_account_id = fields.Many2one(
        string="Impairment Account",
        comodel_name="account.account",
        domain=[
            ("type", "=", "other"),
        ],
    )
    impairment_expense_account_id = fields.Many2one(
        string="Impairment Expense Account",
        comodel_name="account.account",
        domain=[
            ("type", "=", "other"),
        ],
    )
    impairment_reversal_account_id = fields.Many2one(
        string="Impairment Expense Reversal Account",
        comodel_name="account.account",
        domain=[
            ("type", "=", "other"),
        ],
    )
    impairment_journal_id = fields.Many2one(
        string="Impairment Journal",
        comodel_name="account.journal",
    )

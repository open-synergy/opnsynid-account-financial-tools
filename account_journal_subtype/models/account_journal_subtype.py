# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountJournalSubtype(models.Model):
    _name = "account.journal_subtype"
    _description = "Account Journal Subtype"

    name = fields.Char(
        string="Journal Subtype",
        required=True,
    )
    type = fields.Selection(
        string="Journal Type",
        selection=[
            ("sale", "Sale"),
            ("sale_refund", "Sale Refund"),
            ("purchase", "Purchase"),
            ("purchase_refund", "Purchase Refund"),
            ("cash", "Cash"),
            ("bank", "Bank and Checks"),
            ("general", "General"),
            ("situation", "Opening/Closing Situation"),
        ],
        required=True,
        default="general",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )

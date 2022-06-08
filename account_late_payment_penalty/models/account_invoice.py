# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    late_payment_penalty_type_ids = fields.Many2many(
        string="Applicable Late Payment Penalty Types",
        comodel_name="account.late_payment_penalty_type",
        relation="rel_invoice_2_late_payment_penalty_type",
        column1="invoice_id",
        column2="late_payment_type_id",
    )

    @api.multi
    def action_move_create(self):
        _super = super(AccountInvoice, self)
        _super.action_move_create()
        for document in self:
            if document.type in ["out_invoice", "in_refund"]:
                aml = document.move_id.line_id.filtered(
                    lambda r: r.account_id.id == document.account_id.id
                    and r.debit > 0.0
                )[0]
            else:
                aml = document.move_id.line_id.filtered(
                    lambda r: r.account_id.id == document.account_id.id
                    and r.credit > 0.0
                )[0]
            type_ids = document.late_payment_penalty_type_ids.ids
            aml.write(
                {
                    "late_payment_penalty_type_ids": [(6, 0, type_ids)],
                }
            )

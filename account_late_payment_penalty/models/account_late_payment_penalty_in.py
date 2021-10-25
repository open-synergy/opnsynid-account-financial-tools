# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountInLatePaymentPenalty(models.Model):
    _name = "account.in_late_payment_penalty"
    _inherit = "account.common_late_payment_penalty"
    _description = "In Late Payment Penalty Type"

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_direction(self):
        _super = super(AccountInLatePaymentPenalty, self)
        _super._compute_direction()

    @api.multi
    @api.depends(
        "move_line_id.date_maturity",
    )
    def _compute_move_date_due(self):
        _super = super(AccountInLatePaymentPenalty, self)
        _super._compute_move_date_due()

    @api.multi
    @api.depends(
        "move_line_id.debit",
        "move_line_id.credit",
    )
    def _compute_move_amount_base(self):
        _super = super(AccountInLatePaymentPenalty, self)
        _super._compute_move_amount_base()

    penalty_move_id = fields.Many2one(
        related="penalty_move_line_id.move_id",
        store=True,
    )

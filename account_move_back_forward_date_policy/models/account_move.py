# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.multi
    def post(self):
        _super = super(AccountMove, self)
        _super.post()
        for doc in self:
            doc.write({"state": doc.state})

    @api.constrains(
        "date",
        "state",
    )
    def _check_back_date(self):
        for doc in self:
            today = fields.Date.from_string(fields.Date.today())
            entry_date = fields.Date.from_string(doc.date)
            if not doc.journal_id.allow_back_date and \
                    entry_date < today:
                msg = _("Back date is not allowed")
                raise UserError(msg)

    @api.constrains(
        "date",
        "state",
    )
    def _check_forward_date(self):
        for doc in self:
            today = fields.Date.from_string(fields.Date.today())
            entry_date = fields.Date.from_string(doc.date)
            if not doc.journal_id.allow_forward_date and \
                    entry_date > today:
                msg = _("Forward date is not allowed")
                raise UserError(msg)

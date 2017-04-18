# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends(
        "state",
        "journal_id.open_group_ids",
        "journal_id.refund_group_ids",
        "journal_id.cancel_group_ids",
        "journal_id.set_to_draft_group_ids",
        "journal_id.re_open_group_ids",
        "journal_id.send_email_group_ids",
        "journal_id.proforma_group_ids"
    )
    def _compute_policy(self):
        user_id = self.env.user.id
        for invoice in self:
            journal = invoice.journal_id
            if user_id == SUPERUSER_ID:
                invoice.open_ok = True
                invoice.refund_ok = True
                invoice.cancel_ok = True
                invoice.set_to_draft_ok = True
                invoice.re_open_ok = True
                invoice.send_email_ok = True
                invoice.proforma_ok = True
                continue

            invoice.open_ok =\
                self._button_policy(journal, 'open')
            invoice.refund_ok =\
                self._button_policy(journal, 'refund')
            invoice.cancel_ok =\
                self._button_policy(journal, 'cancel')
            invoice.set_to_draft_ok =\
                self._button_policy(journal, 'set_to_draft')
            invoice.re_open_ok =\
                self._button_policy(journal, 're_open')
            invoice.send_email_ok =\
                self._button_policy(journal, 'send_email')
            invoice.proforma_ok =\
                self._button_policy(journal, 'proforma')

    @api.model
    def _button_policy(self, journal, button_type):
        result = False
        user = self.env.user
        group_ids = user.groups_id.ids

        if button_type == 'open':
            button_group_ids = journal.open_group_ids.ids
        elif button_type == 'refund':
            button_group_ids = journal.refund_group_ids.ids
        elif button_type == 'cancel':
            button_group_ids = journal.cancel_group_ids.ids
        elif button_type == 'set_to_draft':
            button_group_ids = journal.set_to_draft_group_ids.ids
        elif button_type == 're_open':
            button_group_ids = journal.re_open_group_ids.ids
        elif button_type == 'send_email':
            button_group_ids = journal.send_email_group_ids.ids
        elif button_type == 'proforma':
            button_group_ids = journal.proforma_group_ids.ids

        if not button_group_ids:
            result = True
        else:
            if (set(button_group_ids) & set(group_ids)):
                result = True
        return result

    open_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        store=False,
    )
    refund_ok = fields.Boolean(
        string="Can Refund",
        compute="_compute_policy",
        store=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    set_to_draft_ok = fields.Boolean(
        string="Can Set To Draft",
        compute="_compute_policy",
        store=False,
    )
    re_open_ok = fields.Boolean(
        string="Can Re-Open",
        compute="_compute_policy",
        store=False,
    )
    send_email_ok = fields.Boolean(
        string="Can Send by Email",
        compute="_compute_policy",
        store=False,
    )
    proforma_ok = fields.Boolean(
        string="Can PRO-FORMA",
        compute="_compute_policy",
        store=False,
    )

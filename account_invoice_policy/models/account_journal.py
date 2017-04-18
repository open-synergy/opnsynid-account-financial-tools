# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    open_group_ids = fields.Many2many(
        string="Allowed to Validate",
        comodel_name="res.groups",
        rel="rel_account_invoice_open",
        col1="type_id",
        col2="group_id",
    )

    refund_group_ids = fields.Many2many(
        string="Allowed to Refund",
        comodel_name="res.groups",
        rel="rel_account_invoice_refund",
        col1="type_id",
        col2="group_id",
    )

    cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        rel="rel_account_invoice_cancel",
        col1="type_id",
        col2="group_id",
    )

    set_to_draft_group_ids = fields.Many2many(
        string="Allowed to Set To Draft",
        comodel_name="res.groups",
        rel="rel_account_invoice_set_to_draft",
        col1="type_id",
        col2="group_id",
    )

    re_open_group_ids = fields.Many2many(
        string="Allowed to Re-Open",
        comodel_name="res.groups",
        rel="rel_account_invoice_re_open",
        col1="type_id",
        col2="group_id",
    )

    send_email_group_ids = fields.Many2many(
        string="Allowed to Send by Email",
        comodel_name="res.groups",
        rel="rel_account_invoice_send_email",
        col1="type_id",
        col2="group_id",
    )

    proforma_group_ids = fields.Many2many(
        string="Allowed to PRO-FORMA",
        comodel_name="res.groups",
        rel="rel_account_invoice_proforma",
        col1="type_id",
        col2="group_id",
    )

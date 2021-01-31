# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Late Payment Penalty",
    "version": "8.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_move_line_day_overdue",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_print_policy",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/ir_cron_data.xml",
        "menu.xml",
        "views/account_late_payment_penalty_type_views.xml",
        "views/account_late_payment_penalty_views.xml",
        "views/account_late_payment_penalty_out_views.xml",
        "views/account_late_payment_penalty_in_views.xml",
        "views/account_move_line_views.xml",
        "views/account_invoice_views.xml",
    ],
}

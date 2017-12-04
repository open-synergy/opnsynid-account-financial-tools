# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Cash Flow Code",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_cash_flow_code_views.xml",
        "views/account_account_views.xml",
        "views/account_move_line_views.xml",
        "views/account_move_views.xml"
    ],
}

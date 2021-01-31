# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Bank Statement Print Policy",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "account_accountant",
        "base_print_policy",
    ],
    "data": [
        "views/account_bank_statement_view.xml",
    ],
}

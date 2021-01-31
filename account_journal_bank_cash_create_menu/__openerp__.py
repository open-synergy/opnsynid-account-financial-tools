# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Create Menu for Journals Bank or Cash",
    "version": "8.0.1.0.0",
    "summary": "Create Menu for Journals Bank or Cash",
    "category": "Accounting Management",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account"],
    "data": [
        "views/account_journal_bank_cash_create_menu.xml",
        "views/account_journal_view.xml",
    ],
}

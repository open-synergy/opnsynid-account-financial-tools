# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Reconcilliation Analytic",
    "version": "11.0.1.0.1",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account"
    ],
    "data": [
        'views/assets_backend.xml',
    ],
    'qweb': [
        'static/src/xml/account_reconciliation.xml',
    ],
    "demo": [],
    "images": [
    ],
}

# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Account Asset Management Monkeypatch",
    "version": "8.0.2.3.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management",
    ],
    "external_dependencies": {
        "python": [
            "numpy",
        ]
    },
    "data": [
        "data/decimal_precision_data.xml",
        "views/account_asset_views.xml",
    ],
}

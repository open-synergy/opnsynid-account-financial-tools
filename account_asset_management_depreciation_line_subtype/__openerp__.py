# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Depreciation Line Subtype",
    "version": "8.0.1.1.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management_extend",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_asset_asset_views.xml",
    ],
}

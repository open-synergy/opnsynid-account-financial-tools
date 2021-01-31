# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fixed Asset QR Code",
    "version": "8.0.1.2.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management",
        "base_qr_code",
    ],
    "data": [
        "data/base_qr_content_policy_data.xml",
        "views/account_asset_views.xml",
    ],
}

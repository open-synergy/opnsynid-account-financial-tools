# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Account Asset + Queue Integration",
    "version": "11.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset",
        "queue_job_batch",
    ],
    "data": [
        "wizards/asset_depreciation_confirmation_wizard_views.xml",
    ],
}

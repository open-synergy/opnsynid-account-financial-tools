# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fixed Asset Retirement",
    "version": "8.0.2.0.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management",
        "base_sequence_configurator",
        "base_workflow_policy",
        "web_readonly_bypass",
        "base_print_policy",
    ],
    "data": [
        "security/res_groups_data.xml",
        "security/ir.model.access.csv",
        "menu.xml",
        "views/account_asset_retirement_type_views.xml",
        "views/account_asset_retirement_common_views.xml",
    ],
}

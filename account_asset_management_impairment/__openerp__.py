# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fixed Asset Impairment",
    "version": "8.0.3.0.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management_config_page",
        "account_asset_management_depreciation_line_subtype",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_print_policy",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "views/account_asset_config_setting_views.xml",
        "views/account_asset_category_views.xml",
        "views/account_asset_views.xml",
        "views/account_asset_impairment_common_views.xml",
        "views/account_asset_impairment_views.xml",
        "views/account_asset_impairment_reversal_views.xml",
    ],
}

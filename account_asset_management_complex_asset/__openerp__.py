# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Complex Fixed Assets Management",
    "version": "8.0.2.3.0",
    "category": "Accounting & Finance",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management_config_page",
        "account_asset_management_depreciation_line_subtype",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "views/account_asset_config_setting_views.xml",
        "views/account_asset_views.xml",
        "views/account_asset_category_views.xml",
        "views/account_complex_asset_movement_common_views.xml",
        "views/account_complex_asset_installation_views.xml",
        "views/account_complex_asset_removal_views.xml",
    ]
}

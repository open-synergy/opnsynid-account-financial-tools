# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fixed Asset Change of Estimation",
    "version": "8.0.2.0.0",
    "category": "Accounting & Finance",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management_depreciation_line_subtype",
        "account_asset_management_config_page",
        "base_sequence_configurator",
        "base_workflow_policy",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/account_asset_depreciation_line_subtype_data.xml",
        "menu.xml",
        "views/account_asset_asset_views.xml",
        "views/account_asset_config_setting_views.xml",
        "views/account_asset_change_estimation_useful_life_views.xml",
        "views/account_asset_change_estimation_salvage_views.xml",
    ]
}

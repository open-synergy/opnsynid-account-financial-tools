# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fixed Asset Impairment",
    "version": "8.0.1.1.1",
    "category": "Accounting & Finance",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management_config_page",
        "base_sequence_configurator",
        "base_workflow_policy",
    ],
    "data": [
        "security/ir.model.access.csv",
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
    ]
}

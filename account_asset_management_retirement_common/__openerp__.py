# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Fixed Asset Retirement",
    "version": "8.0.1.1.1",
    "category": "Accounting & Finance",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management",
        "base_sequence_configurator",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/account_asset_retirement_type_views.xml",
        "views/account_asset_retirement_common_views.xml",
    ]
}

# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock and Asset Management Integration",
    "version": "8.0.2.0.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_asset_management_extend",
        "stock_account",
    ],
    "data": [
        "wizards/create_fixed_asset_from_lot.xml",
        "wizards/link_fixed_asset_to_lot.xml",
        "views/account_asset_views.xml",
        "views/product_template_views.xml",
        "views/stock_production_lot_views.xml",
        "views/account_asset_config_setting_views.xml",
    ],
}

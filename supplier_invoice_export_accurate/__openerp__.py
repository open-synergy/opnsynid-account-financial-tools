# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Generate XML Supplier Invoice Based On Accurate Format",
    "version": "8.0.1.0.0",
    "category": "Invoicing",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["account"],
    "data": [
        "views/res_company_view.xml",
        "views/supplier_invoice_export_to_accurate.xml",
        "views/account_invoice_views.xml",
        "views/account_payment_term_view.xml",
        "views/product_uom_view.xml"
    ],
}

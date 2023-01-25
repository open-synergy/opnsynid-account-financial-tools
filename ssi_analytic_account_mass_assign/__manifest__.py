# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Analytic Account Mass Assign",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_financial_accounting",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "wizards/account_analytic_mass_assign_view.xml",
    ],
    "demo": [],
}

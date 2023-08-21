# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Analytic Account Mass Assign",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
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

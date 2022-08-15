# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    lock_date_group_ids = fields.Many2many(
        string="Specific groups for advisor",
        comodel_name="res.groups",
        relation="rel_res_company_2_lock_date_group",
        column1="company_id",
        column2="group_id",
    )

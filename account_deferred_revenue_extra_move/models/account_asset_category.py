# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAssetCategory(models.Model):
    _name = "account.asset.category"
    _inherit = [
        "account.asset.category",
    ]

    extra_journal_id = fields.Many2one(
        string="Journal for Extra Accounting Entry",
        comodel_name="account.journal",
        ondelete="restrict",
    )

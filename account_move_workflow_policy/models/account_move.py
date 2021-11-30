# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = [
        "account.move",
        "mixin.policy",
    ]

    @api.multi
    def _compute_policy(self):
        _super = super(AccountMove, self)
        _super._compute_policy()

    # Policy Field
    post_ok = fields.Boolean(
        string="Can Post",
        compute="_compute_policy",
    )
    duplicate_ok = fields.Boolean(
        string="Can Duplicate",
        compute="_compute_policy",
    )
    reverse_ok = fields.Boolean(
        string="Can Reverse Entry",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel Entry",
        compute="_compute_policy",
    )

    @api.onchange(
        "journal_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        for document in self:
            document.policy_template_id = template_id

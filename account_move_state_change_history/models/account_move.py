# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = [
        "account.move",
        "mixin.state_change_history",
    ]

    @api.multi
    def button_cancel(self):
        # Perlu dioverride karena tidak menggunakan ORM write
        _super = super(AccountMove, self)
        res = _super.button_cancel()
        for document in self:
            document.create_state_change_history("cancel")
        return res

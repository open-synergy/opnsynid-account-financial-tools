# Copyright 2022 PT. Simetri Sinergi Indonesia.
# Copyright 2022 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class AccountMove(models.Model):

    _inherit = "account.move"

    @api.multi
    def _check_lock_date(self):
        _super = super(AccountMove, self)
        current_user = self.env.user
        current_group_ids = current_user.groups_id.ids
        for document in self:
            lock_date = max(
                document.company_id.period_lock_date or "0000-00-00",
                document.company_id.fiscalyear_lock_date or "0000-00-00",
            )
            specific_group_ids = document.company_id.lock_date_group_ids.ids
            if specific_group_ids:
                if self.user_has_groups("account.group_account_manager"):
                    if set(specific_group_ids) & set(current_group_ids):
                        lock_date = document.company_id.fiscalyear_lock_date
                if document.date <= (lock_date or "0000-00-00"):
                    if self.user_has_groups("account.group_account_manager"):
                        message = _(
                            "You cannot add/modify entries prior to "
                            "and inclusive of the lock date %s"
                        ) % (lock_date)
                    else:
                        message = _(
                            "You cannot add/modify entries prior to "
                            "and inclusive of the lock date %s. "
                            "Check the company settings or ask "
                            "someone with the 'Adviser' role"
                        ) % (lock_date)
                    raise UserError(message)
            else:
                return _super._check_lock_date()

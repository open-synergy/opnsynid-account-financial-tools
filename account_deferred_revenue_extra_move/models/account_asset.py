# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountAssetAsset(models.Model):
    _name = "account.asset.asset"
    _inherit = [
        "account.asset.asset",
    ]

    extra_move_id = fields.Many2one(
        string="Extra Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        ondelete="restrict",
        copy=False,
    )

    @api.multi
    def action_create_extra_move(self):
        for record in self:
            record._create_extra_move()

    @api.multi
    def action_delete_extra_move(self):
        for record in self:
            record._delete_extra_move()

    @api.multi
    def _create_extra_move(self):
        self.ensure_one()
        obj_move = self.env["account.move"]
        move = obj_move.create(self._prepare_extra_account_move())
        move.post()
        self.write(
            {
                "extra_move_id": move.id,
            }
        )

    @api.multi
    def _delete_extra_move(self):
        self.ensure_one()
        move = self.extra_move_id
        self.write(
            {
                "extra_move_id": False,
            }
        )
        move.unlink()

    @api.multi
    def _get_extra_move_journal(self):
        self.ensure_one()
        error_msg = "_(No extra move journal defined)"
        if not self.category_id.extra_journal_id:
            raise UserError(error_msg)
        return self.category_id.extra_journal_id

    @api.multi
    def _get_extra_move_analytic_account(self):
        self.ensure_one()
        return self.category_id.account_analytic_id

    @api.multi
    def _prepare_extra_account_move(self):
        self.ensure_one()
        journal = self._get_extra_move_journal()
        lines = []
        lines.append(self._prepare_extra_move_debit_move_line_detail())
        lines.append(self._prepare_extra_move_credit_move_line_detail())
        name = "Extra move for deferred revenue %s" % (self.name)
        return {
            "ref": name,
            "journal_id": journal.id,
            "date": self.date,
            "line_ids": lines,
        }

    @api.multi
    def _prepare_extra_move_debit_move_line_detail(self):
        self.ensure_one()
        analytic = self._get_extra_move_analytic_account()
        name = "Extra move for deferred revenue %s" % (self.name)
        return (
            0,
            0,
            {
                "name": name,
                "account_id": self.category_id.account_depreciation_id.id,
                "debit": self.value,
                "credit": 0.0,
                "analytic_account_id": analytic and analytic.id or False,
            },
        )

    @api.multi
    def _prepare_extra_move_credit_move_line_detail(self):
        self.ensure_one()
        analytic = self._get_extra_move_analytic_account()
        name = "Extra move for deferred revenue %s" % (self.name)
        return (
            0,
            0,
            {
                "name": name,
                "account_id": self.category_id.account_depreciation_expense_id.id,
                "credit": self.value,
                "debit": 0.0,
                "analytic_account_id": analytic and analytic.id or False,
            },
        )

# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class AccountMove(models.Model):
    _inherit = ("account.move",)

    @api.multi
    def post(self):
        for record in self:
            ctx = self.env.context.copy()
            invoice = ctx.get("invoice", False)
            if record.name == "/" and not invoice:
                ctx.update(
                    {
                        "ir_sequence_date": record.date,
                    }
                )
            name = record.journal_id.sequence_id.with_context(ctx)._next()
            record.write({"name": name})
        return super(AccountMove, self).post()

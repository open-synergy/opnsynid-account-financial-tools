# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    asset_id = fields.Many2one(
        string="Fixed Asset",
        comodel_name="account.asset.asset",
        ondelete="restrict",
    )

    @api.multi
    def _get_initial_move(self):
        self.ensure_one()
        obj_quant = self.env["stock.quant"]
        quants = obj_quant.search(self._get_initial_move_quant_domain())
        # TODO: Refactor Please
        moves = set()
        for quant in quants:
            moves |= {move for move in quant.history_ids}
        moves = list(moves)
        if len(moves) == 1:
            return moves[0]
        else:
            return False

    @api.multi
    def _get_initial_move_quant_domain(self):
        self.ensure_one()
        return [
            ("lot_id", "=", self.id)
        ]

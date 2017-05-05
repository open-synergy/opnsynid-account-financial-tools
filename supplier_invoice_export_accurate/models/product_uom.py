# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProductUom(models.Model):
    _inherit = "product.uom"

    accurate_uom_code = fields.Char(
        string='Accurate UOM Code'
        )

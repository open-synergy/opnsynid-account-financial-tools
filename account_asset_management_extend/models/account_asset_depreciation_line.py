# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountAssetDepreciationLine(models.Model):
    _inherit = "account.asset.depreciation.line"
    # This will accomodate insertion of Asset Value depreciation type in
    # the middle of table. Thus it will accomodate othe fixed asset
    # event that can happend (e.g. improvement, impairment)
    _order = "line_date, type"

    amount = fields.Float(
        # Remove digits configuration to avoid rounding problems
        # Actual number will store on database
        # ui will only show 2 digits
        digits=False,
    )
    # pylint: disable=locally-disabled, method-compute
    remaining_value = fields.Float(
        # Remove digits configuration to avoid rounding problems
        # Actual number will store on database
        # ui will only show 2 digits
        digits=False,
        compute="_compute",
        store=True,
    )
    # pylint: disable=locally-disabled, method-compute
    depreciated_value = fields.Float(
        # Remove digits configuration to avoid rounding problems
        # Actual number will store on database
        # ui will only show 2 digits
        digits=False,
        compute="_compute",
        store=True,
    )

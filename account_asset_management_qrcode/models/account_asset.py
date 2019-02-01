# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class AccountAssetAsset(models.Model):
    _name = "account.asset.asset"
    _inherit = ["account.asset.asset", "base.qr_document"]

# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class AccountMoveLineAnalysis(models.Model):
    _name = "account.move_line_analysis"
    _description = "Account Move Line Analysis"
    _auto = False
    _order = "date desc"

    date = fields.Date(
        string="Effective Date",
    )
    date_created = fields.Date(
        string="Date Created",
    )
    date_maturity = fields.Date(
        string="Date Maturity",
    )
    ref = fields.Char(
        string="Reference",
    )
    nbr = fields.Integer(
        string="# of Items",
    )
    debit = fields.Float(
        string="Debit",
    )
    credit = fields.Float(
        string="Credit",
    )
    balance = fields.Float(
        string="Balance",
    )
    amount_currency = fields.Float(
        string="Amount Currency",
    )
    period_id = fields.Many2one(
        string="Period",
        comodel_name="account.period",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
    )
    fiscalyear_id = fields.Many2one(
        string="Fiscal Year",
        comodel_name="account.fiscalyear",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    product_uom_id = fields.Many2one(
        string="Product Unit of Measure",
        comodel_name="product.uom",
    )
    move_state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Unposted"),
            ("posted", "Posted"),
        ],
    )
    move_line_state = fields.Selection(
        string="State of Move Line",
        selection=[
            ("draft", "Unbalanced"),
            ("valid", "Valid"),
        ],
    )
    reconcile_id = fields.Many2one(
        string="Reconciliation Number",
        comodel_name="account.move.reconcile",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    quantity = fields.Float(
        string="Products Quantity",
    )
    user_type_id = fields.Many2one(
        string="Account Type",
        comodel_name="account.account.type",
    )
    type = fields.Selection(
        string="Internal Type",
        selection=[
            ("receivable", "Receivable"),
            ("payable", "Payable"),
            ("cash", "Cash"),
            ("view", "View"),
            ("consolidation", "Consolidation"),
            ("other", "Regular"),
            ("closed", "Closed"),
        ],
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
    )

    def _select(self):
        select_str = """
        SELECT
            a.id AS id,
            a.date AS date,
            a.date_maturity AS date_maturity,
            a.date_created AS date_created,
            a.ref AS ref,
            a.move_state AS move_state,
            a.move_line_state AS move_line_state,
            a.reconcile_id AS reconcile_id,
            a.partner_id AS partner_id,
            a.product_id AS product_id,
            a.product_uom_id AS product_uom_id,
            a.company_id AS company_id,
            a.journal_id AS journal_id,
            a.fiscalyear_id AS fiscalyear_id,
            a.period_id AS period_id,
            a.account_id AS account_id,
            a.analytic_account_id AS analytic_account_id,
            a.type AS type,
            a.user_type AS user_type_id,
            a.nbr AS nbr,
            a.quantity AS quantity,
            a.currency_id AS currency_id,
            a.amount_currency AS amount_currency,
            a.debit AS debit,
            a.credit AS credit,
            a.balance AS balance
        """
        return select_str

    def _from(self):
        from_str = """
        account_entries_report AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        """
        return join_str

    def _group_by(self):
        group_str = """
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(),
            self._group_by()
        ))

# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
from lxml import etree
import base64


class SupplierInvoiceExportToAccurate(models.TransientModel):
    _name = "supplier.invoice.export_to_accurate"
    _description = "Supplier Invoice Export To Accurate"

    name = fields.Char(
        string="File Name",
        readonly=True
    )

    data = fields.Binary(
        string="File",
        readonly=True
    )

    state = fields.Selection(
        string="State",
        selection=[
            ('choose', 'choose'),
            ('get', 'get')
        ],
        default="choose"
    )

    @api.multi
    def button_export(self):
        self.ensure_one()
        obj_invoice = self.env['account.invoice']
        invoice_ids = self.env.context['active_ids']

        invoice = obj_invoice.browse(invoice_ids)

        strWarning = _(
            'You have to define a branch code!\n'
            'For more information, please contact administrator.'
        )

        if not invoice.company_id.accurate_branch_code:
            raise UserError(strWarning)

        # Create Element ROOT
        root = etree.Element("NMEXML", {
            "ACCOUNTANTCOPYID": "",
            "BranchCode": invoice.company_id.accurate_branch_code,
            "EximID": "%s" % (invoice.id or ''),
        })
        # Create Element CHILD ROOT
        child_root = etree.SubElement(root, "TRANSACTIONS", {
            "OnError": "CONTINUE"
        })
        # Create Element SUB CHILD ROOT
        sub_child_root = etree.SubElement(child_root, "PURCHASEINVOICE", {
            "REQUESTID": "1",
            "operation": "Add"
        })
        # Create Element account.invoice
        etree.SubElement(sub_child_root, "TRANSACTIONID")

        # Create Element account.invoice
        for invoice_line in invoice.invoice_line:
            # Create Element ROOT account.invoice.line
            line_root = etree.SubElement(sub_child_root, "ITEMLINE", {
                "operation": "Add",
            })
            key_id = etree.SubElement(line_root, "KeyID")
            key_id.text = "%s" % (invoice_line.id or '')

            item_no = etree.SubElement(line_root, "ITEMNO")
            item_no.text = "%s" % (invoice_line.product_id.code or '')

            quantity = etree.SubElement(line_root, "QUANTITY")
            quantity.text = "%s" % (invoice_line.quantity or '')

            item_unit = etree.SubElement(line_root, "ITEMUNIT")
            item_unit.text = "%s" % (invoice_line.uos_id.accurate_uom_code or '')

            unit_ratio = etree.SubElement(line_root, "UNITRATIO")
            unit_ratio.text = "%s" % (invoice_line.uos_id.factor or '')

            etree.SubElement(line_root, "ITEMRESERVED1")

            etree.SubElement(line_root, "ITEMRESERVED2")

            etree.SubElement(line_root, "ITEMRESERVED3")

            etree.SubElement(line_root, "ITEMRESERVED4")

            etree.SubElement(line_root, "ITEMRESERVED5")

            etree.SubElement(line_root, "ITEMRESERVED6")

            etree.SubElement(line_root, "ITEMRESERVED7")

            etree.SubElement(line_root, "ITEMRESERVED8")

            etree.SubElement(line_root, "ITEMRESERVED9")

            etree.SubElement(line_root, "ITEMRESERVED10")

            item_mov_desc =\
                etree.SubElement(line_root, "ITEMOVDESC")
            item_mov_desc.text =\
                "%s" % (invoice_line.name or '')

            unit_price =\
                etree.SubElement(line_root, "UNITPRICE")
            unit_price.text = "%s" % (invoice_line.price_unit or '')

            item_disc_pc =\
                etree.SubElement(line_root, "ITEMDISCPC")
            item_disc_pc.text = "%s" % (invoice_line.discount or '')

            tax_codes =\
                etree.SubElement(line_root, "TAXCODES")
            if invoice_line.invoice_line_tax_id:
                tax_codes.text = "T"

            etree.SubElement(line_root, "POSEQ")

            bruto_unit_price =\
                etree.SubElement(line_root, "BRUTOUNITPRICE")
            subtotal = invoice_line.price_subtotal
            qty = invoice_line.quantity
            bruto_unit_price.text =\
                "%s" % ((subtotal/qty) or '')

            WH1 =\
                etree.SubElement(line_root, "WAREHOUSEID")
            WH1.text = "%s" % ("CENTRE" or '')

            etree.SubElement(line_root, "QTYCONTROL")

        invoice_no = etree.SubElement(sub_child_root, "INVOICENO")
        invoice_no.text = "%s" % (invoice.number or '')

        invoice_date = etree.SubElement(sub_child_root, "INVOICEDATE")
        invoice_date.text = "%s" % (invoice.date_invoice or '')

        tax1ID =\
            etree.SubElement(sub_child_root, "TAX1ID")

        tax1Code =\
            etree.SubElement(sub_child_root, "TAX1CODE")
        if invoice.tax_line:
            tax1ID.text = "T"
            tax1Code.text = "T"

        etree.SubElement(sub_child_root, "TAX2CODE")

        tax1rate =\
            etree.SubElement(sub_child_root, "TAX1RATE")
        tax1rate.text = "10"

        tax2rate =\
            etree.SubElement(sub_child_root, "TAX2RATE")
        tax2rate.text = "1"

        rate =\
            etree.SubElement(sub_child_root, "RATE")
        rate.text = "1"

        inclusivetax =\
            etree.SubElement(sub_child_root, "INCLUSIVETAX")
        inclusivetax.text = "0"

        invtaxable =\
            etree.SubElement(sub_child_root, "INVOICEISTAXABLE")
        invtaxable.text = "1"

        cashdisc =\
            etree.SubElement(sub_child_root, "CASHDISCOUNT")
        cashdisc.text = "0"

        etree.SubElement(sub_child_root, "CASHDISCPC")

        invoice_amount =\
            etree.SubElement(sub_child_root, "INVOICEAMOUNT")
        invoice_amount.text = "%s" % (invoice.amount_total or '')

        terms_id =\
            etree.SubElement(sub_child_root, "TERMSID")
        if invoice.payment_term:
            data_termsid = invoice.payment_term.accurate_termsid
        else:
            data_termsid = "COD"
        terms_id.text =\
            "%s" % (data_termsid or '')

        etree.SubElement(sub_child_root, "FOB")

        purchase_order_no =\
            etree.SubElement(sub_child_root, "PURCHASEORDERNO")
        purchase_order_no.text = "%s" % (invoice.origin or '')

        WH2 =\
            etree.SubElement(sub_child_root, "WAREHOUSEID")
        WH2.text = "CENTRE"

        description = etree.SubElement(sub_child_root, "DESCRIPTION")
        description.text = "%s" % (invoice.name or '')

        etree.SubElement(sub_child_root, "SHIPDATE")

        posted = etree.SubElement(sub_child_root, "POSTED")
        posted.text = "%s" % ('1')

        fiscal_rate =\
            etree.SubElement(sub_child_root, "FISCALRATE")
        fiscal_rate.text = "%s" % ('1')

        etree.SubElement(sub_child_root, "INVFROMPR")

        tax_date = etree.SubElement(sub_child_root, "TAXDATE")
        tax_date.text = "%s" % (invoice.date_invoice or '')

        vendor_id = etree.SubElement(sub_child_root, "VENDORID")
        vendor_id.text = "%s" % (invoice.commercial_partner_id.ref or '')

        sequenceno =\
            etree.SubElement(sub_child_root, "SEQUENCENO")
        sequenceno.text = "%s" % (invoice.number or '')

        ap_account = etree.SubElement(sub_child_root, "APACCOUNT")
        ap_account.text = "%s" % (invoice.account_id.code or '')

        etree.SubElement(sub_child_root, "SHIPVENDID")

        invtaxno1 =\
            etree.SubElement(sub_child_root, "INVTAXNO1")
        invtaxno1.text = "000"

        invtaxno2 =\
            etree.SubElement(sub_child_root, "INVTAXNO2")
        invtaxno2.text = "000"

        etree.SubElement(sub_child_root, "SSPDATE")

        etree.SubElement(sub_child_root, "EXPENSESOFBILLID")

        etree.SubElement(sub_child_root, "EXPENSESJOURNALDATETYPE")

        etree.SubElement(sub_child_root, "LOCKED_BY")

        etree.SubElement(sub_child_root, "LOCKED_TIME")

        data_xml = etree.tostring(root)
        vals = {
            "state": "get",
            "data": base64.b64encode(data_xml.encode('utf8')),
            "name": "__export__." + invoice.number + ".xml"
        }
        self.write(vals)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'supplier.invoice.export_to_accurate',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

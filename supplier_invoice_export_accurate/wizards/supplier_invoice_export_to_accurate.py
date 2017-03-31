# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
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

        # Create Element ROOT
        root = etree.Element("NMEXML", {
            "EximID": "",
            "BranchCode": invoice.company_id.accurate_branch_code,
            "ACCOUNTANTCOPYID": ""
        })
        # Create Element CHILD ROOT
        child_root = etree.SubElement(root, "TRANSACTIONS", {
            "OnError": "CONTINUE"
        })
        # Create Element SUB CHILD ROOT
        sub_child_root = etree.SubElement(child_root, "PURCHASEINVOICE", {
            "operation": "Add",
            "REQUESTID": ""
        })
        # Create Element account.invoice
        etree.SubElement(sub_child_root, "TRANSACTIONID")

        invoice_no = etree.SubElement(sub_child_root, "INVOICENO")
        invoice_no.text = "%s" % (invoice.supplier_invoice_number or '')

        invoice_date = etree.SubElement(sub_child_root, "INVOICEDATE")
        invoice_date.text = "%s" % (invoice.date_invoice or '')

        etree.SubElement(sub_child_root, "TAX1ID")

        etree.SubElement(sub_child_root, "TAX1CODE")

        etree.SubElement(sub_child_root, "TAX2CODE")

        etree.SubElement(sub_child_root, "TAX1RATE")

        etree.SubElement(sub_child_root, "TAX2RATE")

        etree.SubElement(sub_child_root, "RATE")

        etree.SubElement(sub_child_root, "INCLUSIVETAX")

        etree.SubElement(sub_child_root, "INVOICEISTAXABLE")

        etree.SubElement(sub_child_root, "CASHDISCOUNT")

        etree.SubElement(sub_child_root, "CASHDISCPC")

        invoice_amount =\
            etree.SubElement(sub_child_root, "INVOICEAMOUNT")
        invoice_amount.text = "%s" % (invoice.amount_total or '')

        terms_id =\
            etree.SubElement(sub_child_root, "TERMSID")
        terms_id.text = "%s" % (invoice.payment_term.name or '')

        etree.SubElement(sub_child_root, "FOB")

        purchase_order_no =\
            etree.SubElement(sub_child_root, "PURCHASEORDERNO")
        purchase_order_no.text = "%s" % (invoice.origin or '')

        etree.SubElement(sub_child_root, "WAREHOUSEID")

        description = etree.SubElement(sub_child_root, "DESCRIPTION")
        description.text = "%s" % (invoice.name or '')

        etree.SubElement(sub_child_root, "SHIPDATE")

        posted = etree.SubElement(sub_child_root, "POSTED")
        posted.text = "%s" % ('1')

        fiscal_rate =\
            etree.SubElement(sub_child_root, "FISCALRATE")
        fiscal_rate.text = "%s" % ('0')

        etree.SubElement(sub_child_root, "INVFROMPR")

        tax_date = etree.SubElement(sub_child_root, "TAXDATE")
        tax_date.text = "%s" % (invoice.date_invoice or '')

        vendor_id = etree.SubElement(sub_child_root, "VENDORID")
        vendor_id.text = "%s" % (invoice.partner_id.ref or '')

        etree.SubElement(sub_child_root, "SEQUENCENO")

        ap_account = etree.SubElement(sub_child_root, "APACCOUNT")
        ap_account.text = "%s" % (invoice.account_id.code or '')

        etree.SubElement(sub_child_root, "SHIPVENDID")

        etree.SubElement(sub_child_root, "INVTAXNO1")

        etree.SubElement(sub_child_root, "INVTAXNO2")

        etree.SubElement(sub_child_root, "SSPDATE")

        etree.SubElement(sub_child_root, "EXPENSESOFBILLID")

        etree.SubElement(sub_child_root, "EXPENSESJOURNALDATETYPE")

        etree.SubElement(sub_child_root, "LOCKED_BY")

        etree.SubElement(sub_child_root, "LOCKED_TIME")

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
            item_unit.text = "%s" % (invoice_line.uos_id.name or '')

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

            etree.SubElement(line_root, "ITEMOVDESC")

            unit_price =\
                etree.SubElement(line_root, "UNITPRICE")
            unit_price.text = "%s" % (invoice_line.price_unit or '')

            item_disc_pc =\
                etree.SubElement(line_root, "ITEMDISCPC")
            item_disc_pc.text = "%s" % (invoice_line.discount or '')

            etree.SubElement(line_root, "TAXCODES")

            etree.SubElement(line_root, "POSEQ")

            etree.SubElement(line_root, "BRUTOUNITPRICE")

            etree.SubElement(line_root, "WAREHOUSEID")

            etree.SubElement(line_root, "QTYCONTROL")

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

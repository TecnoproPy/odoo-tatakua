# Copyright 2020 jeo Software Jorge Obiols <jorge.obiols@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

#   Para correr los tests
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben empezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos para testing como sigue:
#   - Nombre sugerido: [nombre cliente]_test
#   - Debe ser creada con Load Demostration Data chequeado
#   - Usuario admin y password admin
#   - El modulo que se quiere testear debe estar instalado.
#
#   Arrancar el test con:
#
#   oe -Q l10n_py_vat_book -c test13 -d test13_test
#

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import datetime


class DocumentTestCase(TransactionCase):
    def setup_invoices(self):
        tax_00 = self.env['account.tax'].search(
            [('type_tax_use', '=', 'sale'), ('amount', '=', 0)], limit=1)
        tax_05 = self.env['account.tax'].search(
            [('type_tax_use', '=', 'sale'), ('amount', '=', 5)], limit=1)
        tax_10 = self.env['account.tax'].search(
            [('type_tax_use', '=', 'sale'), ('amount', '=', 10)], limit=1)

        inv = self.env.ref('l10n_py_vat_book.demo_vat_invoice_1')
        inv.invoice_line_ids[0].tax_ids = tax_05
        inv.invoice_line_ids[1].tax_ids = tax_05

        inv = self.env.ref('l10n_py_vat_book.demo_vat_invoice_2')
        inv.invoice_line_ids[0].tax_ids = tax_10
        inv.invoice_line_ids[1].tax_ids = tax_10

        inv = self.env.ref('l10n_py_vat_book.demo_vat_invoice_3')
        inv.invoice_line_ids[0].tax_ids = tax_10
        inv.invoice_line_ids[1].tax_ids = tax_10
        inv.invoice_line_ids[2].tax_ids = tax_00

        inv = self.env.ref('l10n_py_vat_book.demo_vat_invoice_4')
        inv.invoice_line_ids[0].tax_ids = tax_05
        inv.invoice_line_ids[1].tax_ids = tax_10
        inv.invoice_line_ids[2].tax_ids = tax_00
        inv.invoice_line_ids[3].tax_ids = tax_00

        inv = self.env.ref('l10n_py_vat_book.demo_vat_invoice_bad')
        inv.invoice_line_ids[0].tax_ids = tax_05
        inv.invoice_line_ids[1].tax_ids = False

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        # Forzar pais Paraguay en el usuario y cargar el template
        _ = self.env['res.company'].create({'name': 'MyCompany'})
        self.env.user.company_id = _
        self.env.user.company_id.country_id = self.env.ref('base.py')
        self.env.ref('l10n_py.py_chart_template').try_loading()

        # import wdb;wdb.set_trace()
        self.setup_invoices()

        vat_journal = self.env.ref('l10n_py_vat_book.demo_vat_journal')
        vat_journal.company_id.country_id = self.env.ref('base.py')
        journals = self.env['account.journal'].search(
            [('id', '=', vat_journal.id)])
        for journal in journals:
            journal.write({'l10n_latam_use_documents': True})

    def validate_invoices(self):
        bad_invoice = self.env.ref('l10n_py_vat_book.demo_vat_invoice_bad')
        demo_journal = self.env.ref('l10n_py_vat_book.demo_vat_journal')
        domain = [('id', '!=', bad_invoice.id),
                  ('journal_id', '=', demo_journal.id)]

        invoices = self.env['account.move'].search(domain)
        self.assertEqual(len(invoices), 4, 'Debe haber solo cuatro registros')

        # Validar todas las facturas
        for invoice in invoices:
            invoice.action_post()

        avl_obj = self.env['account.ar.vat.line']

        invoice1 = self.env.ref('l10n_py_vat_book.demo_vat_invoice_1')
        invoice2 = self.env.ref('l10n_py_vat_book.demo_vat_invoice_2')
        invoice3 = self.env.ref('l10n_py_vat_book.demo_vat_invoice_3')
        invoice4 = self.env.ref('l10n_py_vat_book.demo_vat_invoice_4')
        self.avl1 = avl_obj.search([('move_id', '=', invoice1.id)])
        self.avl2 = avl_obj.search([('move_id', '=', invoice2.id)])
        self.avl3 = avl_obj.search([('move_id', '=', invoice3.id)])
        self.avl4 = avl_obj.search([('move_id', '=', invoice4.id)])

    def test_01_check_date(self):
        self.validate_invoices()

        date = datetime.today().strftime('%Y-%m') + '-01'
        self.assertEqual(self.avl1.date.strftime('%Y-%m-%d'), date)
        self.assertEqual(self.avl2.date.strftime('%Y-%m-%d'), date)
        self.assertEqual(self.avl3.date.strftime('%Y-%m-%d'), date)
        self.assertEqual(self.avl4.date.strftime('%Y-%m-%d'), date)

    def test_02_check_ruc(self):
        self.validate_invoices()

        self.assertEqual(self.avl1.ruc, '80021359-9')
        self.assertEqual(self.avl2.ruc, '80021359-9')
        self.assertEqual(self.avl3.ruc, '80021359-9')
        self.assertEqual(self.avl4.ruc, '80021359-9')

    def test_03_check_base5(self):
        self.validate_invoices()
        self.assertAlmostEqual(self.avl1.base_5, -169.524, places=1)
        self.assertAlmostEqual(self.avl2.base_5, 0, places=1)
        self.assertAlmostEqual(self.avl3.base_5, 0, places=1)
        self.assertAlmostEqual(self.avl4.base_5, -111.429, places=1)

    def test_04_check_base10(self):
        self.validate_invoices()
        # Testear base10
        self.assertAlmostEqual(self.avl1.base_10, 0, places=1)
        self.assertAlmostEqual(self.avl2.base_10, -143.64, places=1)
        self.assertAlmostEqual(self.avl3.base_10, -124.55, places=1)
        self.assertAlmostEqual(self.avl4.base_10, -127.27, places=1)

    def test_05_check_vat5(self):
        self.validate_invoices()
        # Testear iva5
        self.assertAlmostEqual(self.avl1.vat_5, -8.476, places=1)
        self.assertAlmostEqual(self.avl2.vat_5, 0, places=1)
        self.assertAlmostEqual(self.avl3.vat_5, 0, places=1)
        self.assertAlmostEqual(self.avl4.vat_5, -5.57, places=1)

    def test_06_check_vat10(self):
        self.validate_invoices()
        # Testear iva10
        self.assertAlmostEqual(self.avl1.vat_10, 0, places=1)
        self.assertAlmostEqual(self.avl2.vat_10, -14.36, places=1)
        self.assertAlmostEqual(self.avl3.vat_10, -12.45, places=1)
        self.assertAlmostEqual(self.avl4.vat_10, -12.73, places=1)

    def test_07_check_not_taxed(self):
        self.validate_invoices()
        # Testear not_taxed
        self.assertAlmostEqual(self.avl1.not_taxed, 0, places=1)
        self.assertAlmostEqual(self.avl2.not_taxed, 0, places=1)
        self.assertAlmostEqual(self.avl3.not_taxed, -96.0, places=1)
        self.assertAlmostEqual(self.avl4.not_taxed, -357.0, places=1)

    def test_08_check_total(self):
        self.validate_invoices()
        # Testear total
        self.assertAlmostEqual(self.avl1.total, -178.00, places=1)
        self.assertAlmostEqual(self.avl2.total, -158.00, places=1)
        self.assertAlmostEqual(self.avl3.total, -233.00, places=1)
        self.assertAlmostEqual(self.avl4.total, -614.00, places=1)

    def test_09_no_vat_exception(self):
        # me traigo la factura mal hecha (le falta iva en la segunda linea)
        bad_invoice = self.env.ref('l10n_py_vat_book.demo_vat_invoice_bad')
        domain = [('id', '=', bad_invoice.id)]
        invoices = self.env['account.move'].search(domain)

        # valido la factura y tiene que fallar porque le falta esa linea
        with self.assertRaises(UserError):
            invoices[0].action_post()

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


class DocumentTestCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        journals = self.env['account.journal'].search([])
        for journal in journals:
            journal.write({'l10n_latam_use_documents': True})

    def validate_invoices(self):
        domain = [('id', '!=', self.env.ref('l10n_py_vat_book.demo_vat_invoice_bad').id)]
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

        self.assertEqual(self.avl1.date.strftime('%Y-%m-%d'), '2020-01-01')
        self.assertEqual(self.avl2.date.strftime('%Y-%m-%d'), '2020-01-01')
        self.assertEqual(self.avl3.date.strftime('%Y-%m-%d'), '2020-01-01')
        self.assertEqual(self.avl4.date.strftime('%Y-%m-%d'), '2020-01-01')

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
        self.assertAlmostEqual(self.avl1.total, -169.53, places=1)
        self.assertAlmostEqual(self.avl2.total, -143.64, places=1)
        self.assertAlmostEqual(self.avl3.total, -220.55, places=1)
        self.assertAlmostEqual(self.avl4.total, -595.70, places=1)

    def test_09_no_vat_exception(self):
        # me traigo la factura mal hecha (le falta iva en la segunda linea)
        domain = [('id', '=', self.env.ref('l10n_py_vat_book.demo_vat_invoice_bad').id)]
        invoices = self.env['account.move'].search(domain)

        # valido la factura y tiene que fallar porque le falta esa linea
        with self.assertRaises(UserError):
            invoices[0].action_post()

    """
    def test_print(self):
        print()
        self.validate_invoices()
        avl = self.env['account.ar.vat.line'].search([])
        for line in avl:
            print(
                '{} {} {} {} B5={:8} B10={:8} IV5={:8} IV10={:8} EX={:8} TOT={:8}'.format(
                    line.date,
                    line.move_id,
                    line.partner_id,
                    line.ruc,
                    line.base_5,
                    line.base_10,
                    line.vat_5,
                    line.vat_10,
                    line.not_taxed,
                    line.total))
        print()
    """
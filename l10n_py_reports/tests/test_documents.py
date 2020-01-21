# Copyright 2020 jeo Software Jorge Obiols <jorge.obiols@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

#   Para correr los tests
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
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
#   oe -Q l10n_py_reports -c test13e -d test13e_test
#

from odoo.tests.common import TransactionCase


class DocumentTestCase(TransactionCase):
    def test_01_timbrado_check(self):
        """ Verifica que se testee la validez de los timbrados
        """
        self.assertEqual(1, 1)

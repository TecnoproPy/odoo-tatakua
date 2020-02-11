# For copyright and license notices, see __manifest__.py file in module root


from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PartnerType(models.Model):
    _name = 'partner.type'
    _description = 'Definicion de tipos de Partners'

    name = fields.Char(
        help='Tipo de Cliente/Proveedor',
        required=True,
        readonly=True
    )
    ruc_required_person = fields.Boolean(
        string='Obligatorio para individuos',
        required=True,
        help='Indica si el Cliente/Proveedor debe tener su RUC definido '
             'cuando es un individuo.\n'
             'Si no es obligatorio, entonces al facturar se tomará el RUC '
             'consolidado.'
    )
    ruc_required_company = fields.Boolean(
        string='Obligatorio para empresas',
        required=True,
        help='Indica si el Cliente/Proveedor debe tener su RUC definido '
             'cuando es una empresa.\n'
             'Si no es obligatorio, entonces al facturar se tomará el RUC '
             'consolidado.'
    )
    consolidated_ruc = fields.Char(
        string='RUC Consolidado',
        help='En ciertos casos, cuando se permite tener el RUC en blanco se '
             'usara este RUC consolidado.'
    )
    default_account = fields.Many2one(
        'account.account',
        string='Cuenta Predeterminada',
        help='Cuenta contable que se utilizará para este tipo de '
             'Cliente/Proveedor',
        required=True
    )
    applied_to = fields.Selection([
        ('sale', 'Ventas'),
        ('purchase', 'Compras')
    ],
        string='Ambito de Aplicación',
        required=True,
        help='Indica si este tipo de Cliente/Proveedor aplica para venta o '
             'para compra'
    )

    def ruc_required(self, company_type):
        if company_type == 'company':
            return self.ruc_required_company
        elif company_type == 'person':
            return self.ruc_required_person
        else:
            raise Exception('Error Interno')

    @api.constrains('default_account')
    def constraint_default_account(self):
        if not self.default_account.reconcile:
            raise ValidationError('La cuenta predeterminada debe ser '
                                  'conciliable.')

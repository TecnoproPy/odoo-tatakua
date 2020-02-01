# For copyright and license notices, see __manifest__.py file in module root


from odoo import models, fields


class PartnerType(models.Model):
    _name = 'partner.type'
    _description = 'Definicion de tipos de partner'

    name = fields.Char(
        help='Tipo de cliente',
        required=True
    )
    ruc_required_person = fields.Boolean(
        string='Obligatorio para individuos',
        required=True
    )
    ruc_required_company = fields.Boolean(
        string='Obligatorio para empresas',
        required=True
    )
    consolidated_ruc = fields.Char(
        string='RUC Consolidado',
        required=True
    )
    default_account = fields.Many2one(
        'account.account',
        string='Cuenta Predeterminada',
    )
    applied_to = fields.Selection([
        ('sale', 'Ventas'),
        ('purchase', 'Compras')],
        string='Aplicacion',
        required=True
    )

    def ruc_required(self, company_type):
        if company_type == 'company':
            return self.ruc_required_company
        if company_type == 'individual':
            return self.ruc_required_person

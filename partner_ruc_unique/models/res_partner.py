# For copyright and license notices, see __manifest__.py file in module root
from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('ruc')
    def _check_ruc_unique(self):

        # obtener una lista de los ruc consolidados
        consolidated_rucs = []
        partner_types = self.env['partner.type'].search(
            [('consolidated_ruc', '!=', False)])
        for pt in partner_types:
            consolidated_rucs.append(pt.consolidated_ruc)

        for record in self:
            if record.parent_id or not record.ruc:
                continue

            test_condition = (config['test_enable'] and
                              not self.env.context.get('test_ruc'))

            if test_condition:
                continue

            if record.ruc in consolidated_rucs:
                continue

            # si el ruc no es consolidado entonces verificar si hay otro igual
            results = self.env['res.partner'].search_count([
                ('parent_id', '=', False),
                ('ruc', '=', record.ruc),
                ('id', '!=', record.id)
            ])
            if results:
                raise ValidationError(_(
                    "El RUC %s ya existe en otro partner.") % record.ruc)

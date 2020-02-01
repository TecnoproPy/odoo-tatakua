# For copyright and license notices, see __manifest__.py file in module root

from odoo import models, _
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move"

    def action_post(self):
        for line in self.line_ids:
            if not line.exclude_from_invoice_tab:
                if not line.tax_ids:
                    raise UserError(_('Todas las lineas de factura deben '
                                      'tener al menos un impuesto de IVA'))
        super().action_post()

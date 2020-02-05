# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.move"

    timbrado_id = fields.Many2one(
        'timbrado.data',
        help="Numero de timbrado que habilita la factura",
        string='Timbrado'
    )
    l10n_py_trade_code = fields.Char(
        related='journal_id.l10n_py_trade_code',
        help='Campo tecnico para relacionar con el timbrado'
    )
    l10n_py_shipping_point = fields.Char(
        related='journal_id.l10n_py_shipping_point',
        help='Campo tecnico para relacionar con el timbrado'
    )
    document_type_code = fields.Char(
        related='l10n_latam_document_type_id.code',
        help='Campo tecnico para relacionar con el timbrado'
    )
    l10n_py_timbrado = fields.Char(
        string='Timbrado Proveedor',
        help='Numero de timbrado de la factura del proveedor'
    )
    l10n_py_validity_end = fields.Date(
        string='Validez Timbrado',
        help='Fecha de caducidad del timbrado del proveedor'
    )
    payment_cash = fields.Char(
        compute='_compute_payment'
    )
    payment_credit = fields.Char(
        compute='_compute_payment'
    )
    payment_days = fields.Char(
        compute='_compute_payment'
    )
    remision = fields.Char(
        string='Nro de remito'
    )
    document_number = fields.Char(
        help="Campo tecnico con la ultima parte del numero de factura, se usa"
             "para mandar a imprimir cuando es preimpreso",
        compute='_compute_document_number',
        string='Ultima parte del Nro de Factura'
    )

    def _compute_document_number(self):
        for reg in self:
            if reg.name:
                j = reg.name.find('-', reg.name.find('-') + 1)
                reg.document_number = reg.name[j + 1:]

    def _compute_payment(self):
        for rec in self:
            inm_ref = 'account.account_payment_term_immediate'
            if rec.invoice_payment_term_id == self.env.ref(inm_ref):
                rec.payment_cash = 'X'
                rec.payment_credit = ' '
            else:
                rec.payment_cash = ' '
                rec.payment_credit = 'X'
            rec.payment_days = ' '

    @api.onchange('l10n_latam_document_type_id')
    def _onchange_l10n_latam_document_type_id(self):
        """ Poner el timbrado correspondiente cuando cambia el tipo de doc
            o False si no hay ningun timbrado
        """
        for rec in self:
            domain = [
                ('shipping_point', '=', rec.l10n_py_shipping_point),
                ('trade_code', '=', rec.l10n_py_trade_code),
                ('document_type_id.code', '=', rec.document_type_code),
                ('state', '=', 'active')
            ]
            timbrado = self.env['timbrado.data'].search(domain)
            rec.timbrado_id = timbrado[0] if timbrado else False

    def action_post(self):
        """ Este metodo se dispara con el boton Publicar
            Solo para facturas o notas de credito al cliente, Obtener el
            proximo numero de documento de la secuencia.
            Luego llamar al metodo original para que publique
        """
        self.ensure_one()
        if self.type in ['out_invoice', 'out_refund']:

            # verificar el tipo de cliente
            partner_type = self.partner_id.partner_type_id
            if partner_type.applied_to != 'sale':
                raise ValidationError('El tipo de cliente "%s" no esta '
                                      'habilitado para ventas' % self.name)

            # verificar si tengo cuenta por defecto y aplicarla
            if partner_type.default_account:
                for line in self.invoice_line_ids:
                    if not partner_type.default_account.reconcile:
                        raise ValidationError(
                            'Se quiere aplicar la cuenta %s a esta '
                            'operacion.\nEsto no es posible porque la cuenta '
                            'no es reconciliable.'
                            '' % partner_type.default_account.display_name)
                    line.account_id = partner_type.default_account

            # obtener las secuencias definidas en el diario
            sequence_ids = self.journal_id.l10n_py_sequence_ids

            # filtrar la secuencia por el tipo de documento
            type_id = self.l10n_latam_document_type_id
            seq = sequence_ids.filtered(
                lambda x: x.l10n_latam_document_type_id == type_id)

            proximo = seq.number_next
            # chequear numero a validar es mayor que el maximo
            if proximo > self.timbrado_id.end_number:
                raise ValidationError(
                    _('El timbrado ya no es valido, el numero de documento '
                      'que quiere validar esta mas alla del rango.\n'
                      'El proximo numero de factura es %s mientras que el '
                      'rango de validez del timbrado es [%s - %s]') %
                    (proximo, self.timbrado_id.start_number,
                     self.timbrado_id.end_number))

            # chequear numero a validar es menor que el minimo
            if proximo < self.timbrado_id.start_number:
                raise ValidationError(
                    _('El timbrado no es valido. Intenta validar un numero de '
                      'documento que es menor al minimo valido para este '
                      'timbrado.\n'
                      'El proximo numero de factura es %s mientras que el '
                      'rango de validez del timbrado es [%s - %s]') %
                    (proximo, self.timbrado_id.start_number,
                     self.timbrado_id.end_number))

            # numero a validar es igual al maximo, invalidar timbrado
            if proximo == self.timbrado_id.end_number:
                self.timbrado_id.state = 'no_active'

            # poner el numero de documento
            self.l10n_latam_document_number = seq.next_by_id()

        # llamar al metodo original
        super().action_post()

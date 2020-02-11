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

            # verificar si tiene definido el tipo de partner
            if not self.partner_id.partner_type_sale_id:
                raise ValidationError(_('Debe definir el tipo de Cliente '
                                        'en el Formulario de Cliente'))

            # verificar que el tipo de cliente se para ventas
            partner_type = self.partner_id.partner_type_sale_id
            if partner_type.applied_to != 'sale':
                raise ValidationError(_('El tipo de cliente "%s" no esta '
                                        'habilitado para '
                                        'ventas' % partner_type.name))

            # verificar si el ruc del cliente es requerido
            chk = self.partner_id.partner_type_sale_id.ruc_required
            if chk(self.partner_id.company_type) and not self.partner_id.ruc:
                raise ValidationError(_('El RUC es requerido, en este caso no '
                                        'puede quedar en blanco'))

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

            # Chequear que la fecha de la factura este dentro de la validez
            # del timbrado. Hay que chequear despues del post porque antes puede
            # no existir la fecha de la factura.
            start = self.timbrado_id.validity_start
            end = self.timbrado_id.validity_end
            if not (start <= self.invoice_date <= end):
                raise ValidationError(
                    _('La fecha de la factura no esta dentro del rango de '
                      'validez del timbrado.'))

        if self.type in ['in_invoice', 'in_refund']:
            # chequear la longitud y tipo de timbrado

            if len(self.l10n_py_timbrado) != 8:
                raise ValidationError(_('La longitud del timbrado debe ser de '
                                        'ocho digitos'))
            try:
                int(self.l10n_py_timbrado)
            except ValueError:
                raise ValidationError(_('El timbrado debe ser numerico'))

            if self.invoice_date > self.l10n_py_validity_end:
                raise ValidationError(_('La fecha de la factura es posterior '
                                        'a la validez del timbrado'))
            # llamar al metodo original
            super().action_post()

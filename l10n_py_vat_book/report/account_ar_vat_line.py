# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import tools, models, fields


class AccountArVatLine(models.Model):
    """ Base model for new Paraguayan VAT reports.
    The idea is that this lines have all the necessary data and which any
    changes in odoo, this ones will be taken for this cube and then no changes
    will be nedeed in the reports that use this lines.
    A line is created for each accounting entry that is affected by VAT tax.

    Basically which it does is cover the accounting entries into columns
    depending of the information of the taxes and add some other fields
    """

    _name = "account.ar.vat.line"
    _description = "VAT line for Analysis in Paraguayan Localization"
    _auto = False

    date = fields.Date(
        readonly=True,
        string='Fecha'
    )
    move_id = fields.Many2one(
        'account.move',
        string='Documento',
        auto_join=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Razon Social',
        readonly=True,
        auto_join=True
    )
    ruc = fields.Char(
        readonly=True,
        string='R.U.C.'
    )
    base_10 = fields.Monetary(
        readonly=True,
        string='Grav. 10%',
        currency_field='company_currency_id'
    )
    base_5 = fields.Monetary(
        readonly=True,
        string='Grav. 5%',
        currency_field='company_currency_id'
    )
    vat_10 = fields.Monetary(
        readonly=True,
        string='IVA 10%',
        currency_field='company_currency_id'
    )
    vat_5 = fields.Monetary(
        readonly=True,
        string='IVA 5%',
        currency_field='company_currency_id'
    )
    not_taxed = fields.Monetary(
        readonly=True,
        string='No Gravado',
        help='No Gravado, todas las lineas que no tienen iva',
        currency_field='company_currency_id'
    )
    total = fields.Monetary(
        readonly=True,
        currency_field='company_currency_id'
    )
    document_type_id = fields.Many2one(
        'l10n_latam.document.type',
        'Document Type',
        readonly=True
    )
    invoice_date = fields.Date(
        readonly=True
    )
    partner_name = fields.Char(
        readonly=True
    )
    move_name = fields.Char(
        readonly=True
    )
    type = fields.Selection(
        selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ],
        readonly=True
    )
    state = fields.Selection(
        [('draft', 'Unposted'),
         ('posted', 'Posted')],
        'Status',
        readonly=True
    )
    journal_id = fields.Many2one(
        'account.journal',
        'Journal',
        readonly=True,
        auto_join=True
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        readonly=True,
        auto_join=True
    )
    company_currency_id = fields.Many2one(
        related='company_id.currency_id',
        readonly=True
    )

    document_type = fields.Char(
        related='document_type_id.display_name',
        string='Tipo de documento'
    )

    def open_journal_entry(self):
        self.ensure_one()
        return self.move_id.get_formview_action()

    def init(self):
        cr = self._cr
        tools.drop_view_if_exists(cr, self._table)
        # we use tax_ids for base amount instead of tax_base_amount for two
        # reasons:
        # * zero taxes do not create any aml line so we can't get base for
        #   them with tax_base_amount
        # * we use same method as in odoo tax report to avoid any possible
        #   discrepancy with the computed tax_base_amount
        query = """
SELECT
    am.id,
    sum(CASE
            WHEN ntg.name = 'IVA 10%'
            THEN aml.balance ELSE Null END) as vat_10,
    sum(CASE
            WHEN ntg.name = 'IVA 5%'
            THEN aml.balance ELSE Null END) as vat_5,
    sum(CASE
            WHEN btg.name = 'IVA 10%'
            THEN aml.balance ELSE Null END) as base_10,
    sum(CASE
            WHEN btg.name = 'IVA 5%'
            THEN aml.balance ELSE Null END) as base_5,
    sum(CASE
            WHEN btg.name = 'IVA Excento'
            THEN aml.balance ELSE Null END) as not_taxed,
    sum(aml.balance) as total,
    rp.ruc as ruc,
    am.name as move_name,
    rp.name as partner_name,
    am.id as move_id,
    am.type,
    am.date,
    am.invoice_date,
    am.partner_id,
    am.journal_id,
    am.name,
    am.l10n_latam_document_type_id as document_type_id,
    am.state,
    am.company_id
FROM
    account_move_line aml
LEFT JOIN
    account_move as am
    ON aml.move_id = am.id
LEFT JOIN
    -- nt = net tax
    account_tax AS nt
    ON aml.tax_line_id = nt.id
LEFT JOIN
    account_move_line_account_tax_rel AS amltr
    ON aml.id = amltr.account_move_line_id
LEFT JOIN
    -- bt = base tax
    account_tax AS bt
    ON amltr.account_tax_id = bt.id
LEFT JOIN
    account_tax_group AS btg
    ON btg.id = bt.tax_group_id
LEFT JOIN
    account_tax_group AS ntg
    ON ntg.id = nt.tax_group_id
LEFT JOIN
    res_partner AS rp
    ON rp.id = am.partner_id
WHERE
    account_internal_type <> 'receivable' and
    am.type in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund')

GROUP BY
    am.id, rp.id
ORDER BY
    am.date, am.name
"""
        sql = """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, query)
        cr.execute(sql)

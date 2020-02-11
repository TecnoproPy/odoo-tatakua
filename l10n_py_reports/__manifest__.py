{
    'name': 'Reportes Paraguay',
    'version': '13.0.0.0.3',
    'category': 'Localizacion',
    'sequence': 14,
    'author': 'Tecnopro',
    'website': 'tecnopro.com.py',
    'license': 'Other OSI approved licence',
    'summary': 'Reportes, Facturas, Notas de credito, etc',
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
    'depends': [
        'account',
        'l10n_py_invoice_document'
    ],
    'external_dependencies': {
        'python': [
            'num2words',
        ],
    },
    'data': [
        'templates/report_invoice.xml',
        'data/report_paperformat_data.xml'
    ],
    'installable': True,
}

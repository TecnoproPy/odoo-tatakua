{
    'name': 'Reportes Paraguay',
    'version': '13.0.0.0.1',
    'category': 'Localizacion',
    'sequence': 14,
    'author': 'TecnoproPy',
    'website': 'TecnoproPy.com',
    'license': 'Other OSI approved licence',
    'summary': 'Reportes, Facturas, Notas de credito, etc',
    "development_status": "Alpha",  # "Alpha|Beta|Production/Stable|Mature"
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
    'demo': [
    ],
    'installable': True,
}

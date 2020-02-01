{
    'name': 'Libros de IVA Paraguay',
    'version': '13.0.0.0.3',
    'category': 'Localizacion',
    'sequence': 14,
    'author': 'TecnoproPy',
    'website': 'TecnoproPy.com',
    'license': 'Other OSI approved licence',
    'summary': 'Libros de IVA',
    "development_status": "Alpha",  # "Alpha|Beta|Production/Stable|Mature"
    'depends': [
        'l10n_py',
        'l10n_py_reports',
        'l10n_py_invoice_document'
    ],
    'data': [
        'report/account_py_vat_line_views.xml',
        'security/ir.model.access.csv',
        'security/security.xml'
    ],
    'demo': [
        'demo/product_data_demo.xml',
        'demo/invoice_data_demo.xml'
    ],
    'installable': True,
}

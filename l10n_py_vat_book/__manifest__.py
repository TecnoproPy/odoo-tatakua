{
    'name': 'Libros de IVA Paraguay',
    'version': '13.0.0.0.4',
    'category': 'Localizacion',
    'sequence': 14,
    'author': 'Tecnopro',
    'website': 'tecnopro.com.py',
    'license': 'Other OSI approved licence',
    'summary': 'Libros de IVA',
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
    'depends': [
        'l10n_py',
        'l10n_py_reports',
        'l10n_py_invoice_document',
        'account_reports',
    ],
    'data': [
        'report/account_py_vat_line_views.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/account_financial_report_data.xml'
    ],
    'demo': [
        'demo/product_data_demo.xml',
        'demo/invoice_data_demo.xml'
    ],
    'installable': True,
}

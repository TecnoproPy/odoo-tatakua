# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Contabilidad Paraguay',
    'version': '13.0.0.0.2',
    'author': 'TecnoproPy',
    'category': 'Localizacion',
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
    'license': 'Other OSI approved licence',
    'website': 'TecnoproPy.com',
    'summary': 'Modulo base para la localizacion Paraguaya',
    'depends': [
        'account',
        'l10n_latam_invoice_document'
    ],
    'data': [
        'data/l10n_py.xml',
        'data/account.account.template.csv',
        'data/account_tax_group.xml',
        'data/l10n_py_post.xml',
        'data/account_chart_template_data.xml',
    ],
    'demo': [
#        'demo/account_bank_statement_demo.xml',
#        'demo/account_invoice_demo.xml',
#        'demo/account_reconcile_model.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
}

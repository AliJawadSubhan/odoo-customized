{
    'name': 'Markition ZATCA QR Code Fix',
    'version': '19.0.1.0.0',
    'summary': 'Ensures the ZATCA QR code appears on printed/exported Saudi tax invoice PDFs',
    'author': 'Markition',
    'depends': ['l10n_sa', 'l10n_sa_edi'],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'data': [
        'views/report_invoice.xml',
    ],
}

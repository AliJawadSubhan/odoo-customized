{
    'name': 'Markition Branding',
    'version': '19.0.1.0.0',
    'summary': 'Custom login page branding for Markition',
    'author': 'Markition',
    'depends': ['web'],
    'data': [
        'views/login_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'markition_branding/static/src/css/login.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

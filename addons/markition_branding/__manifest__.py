{
    'name': 'Markition Branding',
    'version': '19.0.2.0.0',
    'summary': 'Platform-wide de-branding and Markition identity',
    'author': 'Markition',
    'depends': ['web'],
    'data': [
        'views/login_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'markition_branding/static/src/css/login.css',
        ],
        'web.assets_backend': [
            'markition_branding/static/src/js/user_menu_debrand.js',
        ],
    },
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}

{
    'name': 'Markition Website Debranding',
    'version': '19.0.1.0.0',
    'summary': 'Remove Odoo promotional footer from website pages',
    'author': 'Markition',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': ['templates/disable_odoo.xml'],
    'installable': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
}

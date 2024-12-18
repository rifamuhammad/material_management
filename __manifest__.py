{
    'name': 'Material Registration',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Module for managing material registration',
    'description': """
        This module allows users to:
        * Register new materials
        * View all materials
        * Update existing materials
        * Delete materials
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
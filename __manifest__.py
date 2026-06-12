{
    'name': 'Cars Management',
    'version': '1.0',
    'depends': ['base', 'mail', 'crm', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/car_feature_data.xml',
        'views/car_view.xml',
        'views/car_action.xml',
        'views/car_menu.xml',
        'views/website_templates.xml',
        'data/cron.xml',
    ],
    'installable': True,
}
# -*- coding: utf-8 -*-
{
    'name': "appserver",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/network_server.xml',
        'views/application.xml',
        'views/user.xml',
        'views/application_user.xml',
        'views/organization.xml',
        'views/organization_user.xml',
        'views/service_profile.xml',
        'views/node.xml',
        'views/downlink_queue.xml',
        'views/integration.xml',
        'views/gateway.xml',
        'views/gateway_profile.xml',
        'views/gateway_ping.xml',
        'views/gateway_ping_rx.xml',
        'views/device.xml',
        'views/device_profile.xml',
        'views/device_keys.xml',
        'views/device_activation.xml',
        'views/device_queue.xml',
        'views/device_queue_mapping.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
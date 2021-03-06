# -*- coding: utf-8 -*-
{
    'name': "netserver",

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
        'views/gateway.xml',
        'views/gateway_stats.xml',
        'views/gateway_profile.xml',
        'views/gateway_profile_extra_channel.xml',
        'views/device.xml',
        'views/device_activation.xml',
        'views/device_queue.xml',
        'views/device_profile.xml',
        'views/frame_log.xml',
        'views/channel_configuration.xml',
        'views/extra_channel.xml',
        'views/service_profile.xml',
        'views/routing_profile.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
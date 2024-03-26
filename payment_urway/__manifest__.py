# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "URWAY Payment Gateway",
    'version': '16.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 300,
    'author': "URWAY Technologies",
    'summary': "Allows you to accept mada / VISA / MasterCard via secure payment gateway.",
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_urway_templates.xml',

        'data/payment_provider_data.xml',
    ],
    'application': True,
    'images':['static/description/Banner.jpg'],
    'description': "URWAY Payment Gateway Odoo V16 Plugin",
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}

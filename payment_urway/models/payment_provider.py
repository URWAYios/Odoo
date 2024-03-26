# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hashlib
import hmac
import logging
import pprint

import requests
from werkzeug.urls import url_join

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

SUPPORTED_CURRENCIES = ('SAR', 'USD')

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('urway', "Urway")], ondelete={'urway': 'set default'}
    )

    urway_merchant_key = fields.Char(required_if_provider='urway', groups='base.group_user', string="Merchant Key",
                                     help="Enter Merchant Key provided by URWAY team.")
    urway_terminal_id = fields.Char(required_if_provider='urway', groups='base.group_user', string="Terminal ID",
                                    help="Enter Terminal ID provided by URWAY team.")
    urway_password = fields.Char(required_if_provider='urway',
                                 string='Terminal Password', groups='base.group_user',
                                 help="Enter Terminal password provided by URWAY team.")
    urway_request_url = fields.Char(required_if_provider='urway',
                                    string="Request URL", groups='base.group_user',
                                    help="URL to send request to.")

    @api.model
    def _get_compatible_providers(self, *args, currency_id=None, **kwargs):
        """ Override of payment to unlist Urway acquirers when the currency is not SAR. """
        providers = super()._get_compatible_providers(*args, currency_id=currency_id, **kwargs)
        currency = self.env['res.currency'].browse(currency_id).exists()
        if currency and currency.name not in SUPPORTED_CURRENCIES:
            providers = providers.filtered(lambda p: p.code != 'urway')
        return providers

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'paypal':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_urway.payment_method_urway').id

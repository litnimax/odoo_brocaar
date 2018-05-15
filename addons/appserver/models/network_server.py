# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class NetworkServer(models.Model):
    _name = 'appserver.network_server'
    _table = 'network_server'
    _auto = False
    _rec_name = 'name'

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)
    server = fields.Char(size=255, required=True)
    ca_cert = fields.Text(required=True, default='')
    tls_cert = fields.Text(required=True, default='')
    tls_key = fields.Text(required=True, default='')
    routing_profile_ca_cert = fields.Text(required=True, default='')
    routing_profile_tls_cert = fields.Text(required=True, default='')
    routing_profile_tls_key = fields.Text(required=True, default='')
    gateway_discovery_enabled = fields.Boolean(required=True, default=False)
    gateway_discovery_interval = fields.Integer(required=True, default=0)
    gateway_discovery_tx_frequency = fields.Integer(required=True, default=0)
    gateway_discovery_dr = fields.Integer(required=True, default=0)
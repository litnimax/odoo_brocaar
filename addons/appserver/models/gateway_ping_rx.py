# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GatewayPingRx(models.Model):
    _name = 'appserver.gateway_ping_rx'
    _table = 'gateway_ping_rx'
    _auto = False

    created_at = fields.Datetime(required=True)
    ping_id = fields.Many2one(string='Gateway Ping', required=True, comodel_name='appserver.gateway_ping',
                              ondelete='cascade')
    # TODO gateway_mac must be defined as indicated below
    gateway_mac = fields.Char()
    gateway_mac_ = fields.Many2one(string='Gateway', required=True, comodel_name='appserver.gateway',
                                   ondelete='cascade', compute='_get_gateway_id')
    received_at = fields.Datetime(required=True)
    rssi = fields.Integer(required=True)
    lora_snr = fields.Float(digits=(3, 1), required=True)
    location = fields.Char()
    altitude = fields.Float()

    @api.multi
    def _get_gateway_id(self):
        for self in self:
            mac = self.env['appserver.gateway'].search(
                [('mac', '=', self.gateway_mac)])
            if mac:
                self.gateway_mac_ = mac.id
            else:
                self.gateway_mac_ = False

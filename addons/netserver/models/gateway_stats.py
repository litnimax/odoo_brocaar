# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GatewayStats(models.Model):
    _name = 'netserver.gateway_stats'
    _table = 'gateway_stats'
    _auto = False

    mac = fields.Char()
    mac_ = fields.Many2one(string='Gateway', required=True, comodel_name='netserver.gateway',
                           ondelete='cascade', compute='_get_gateway_id')
    timestamp = fields.Datetime(required=True)
    interval = fields.Char(size=10, required=True)
    rx_packets_received = fields.Integer(required=True)
    rx_packets_received_ok = fields.Integer(required=True)
    tx_packets_received = fields.Integer(required=True)
    tx_packets_emitted = fields.Integer(required=True)

    _sql_constraints = [
        ('mac_unique',
         'UNIQUE(mac)',
         _(u'The mac must be unique')),
        ('timestamp_unique',
         'UNIQUE(timestamp)',
         _(u'The timestamp must be unique')),
        ('interval_unique',
         'UNIQUE(interval)',
         _(u'The interval must be unique')),
    ]

    @api.multi
    def _get_gateway_id(self):
        for self in self:
            mac = self.env['netserver.gateway'].search(
                [('mac', '=', self.mac)])
            if mac:
                self.mac_ = mac.id
            else:
                self.mac_ = False

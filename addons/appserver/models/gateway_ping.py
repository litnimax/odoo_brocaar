# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GatewayPing(models.Model):
    _name = 'appserver.gateway_ping'
    _table = 'gateway_ping'
    _auto = False
    _rec_name = 'dr'

    created_at = fields.Datetime(required=True)
    # TODO gateway_mac must be defined as indicated below
    gateway_mac = fields.Char()
    gateway_mac_ = fields.Many2one(string='Gateway', required=True, comodel_name='appserver.gateway',
                                   ondelete='cascade', compute='_get_gateway_id')
    frequency = fields.Integer(required=True)
    dr = fields.Integer(required=True)

    @api.multi
    def _get_gateway_id(self):
        for self in self:
            mac = self.env['appserver.gateway'].search(
                [('mac', '=', self.gateway_mac)])
            if mac:
                self.gateway_mac_ = mac.id
            else:
                self.gateway_mac_ = False

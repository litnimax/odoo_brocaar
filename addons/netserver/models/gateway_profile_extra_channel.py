# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GatewayProfileExtraChannel(models.Model):
    _name = 'netserver.gateway_profile_extra_channel'
    _table = 'gateway_profile_extra_channel'
    _auto = False

    gateway_profile_id = fields.Char()
    gateway_profile_id_ = fields.Many2one(string='Gateway Profile', required=True,
                                          comodel_name='netserver.gateway_profile', ondelete='cascade',
                                          compute='_get_gateway_profile_id')
    modulation = fields.Char(size=10, required=True)
    frequency = fields.Integer(required=True)
    bandwidth = fields.Integer(required=True)
    bitrate = fields.Integer(required=True)
    spreading_factors = fields.Text()

    @api.multi
    def _get_gateway_profile_id(self):
        for self in self:
            gateway_profile = self.env['netserver.gateway_profile'].search(
                [('gateway_profile_id', '=', self.device_profile_id)])
            if gateway_profile:
                self.gateway_profile_id_ = gateway_profile.id
            else:
                self.gateway_profile_id_ = False
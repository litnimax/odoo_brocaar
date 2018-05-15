# -*- coding: utf-8 -*-
from odoo import models, fields


class ExtraChannel(models.Model):
    _name = 'netserver.extra_channel'
    _table = 'extra_channel'
    _auto = False

    channel_configuration_id = fields.Many2one(string='Channel Configuration', required=True,
                                               comodel_name='netserver.channel_configuration', ondelete='cascade')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    modulation = fields.Char(size=10, required=True)
    frequency = fields.Integer(required=True)
    bandwidth = fields.Integer(required=True)
    bit_rate = fields.Integer(required=True)
    spread_factors = fields.Integer()
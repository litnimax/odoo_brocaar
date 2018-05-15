# -*- coding: utf-8 -*-
from odoo import models, fields


class ChannelConfiguration(models.Model):
    _name = 'netserver.channel_configuration'
    _table = 'channel_configuration'
    _auto = False
    _rec_name = 'name'

    name = fields.Char(size=100, required=True)
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    band = fields.Char(size=20, required=True)
    channels = fields.Integer(required=True)
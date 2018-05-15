# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Organization(models.Model):
    _name = 'appserver.organization'
    _table = 'organization'
    _auto = False
    _rec_name = 'name'

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)
    display_name = fields.Char(size=100, required=True)
    can_have_gateways = fields.Boolean(required=True)

# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class User(models.Model):
    _name = 'appserver.user'
    _table = 'user'
    _auto = False
    _rec_name = 'username'

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    username = fields.Char(size=100, required=True)
    password_hash = fields.Char(size=200, required=True)
    session_ttl = fields.Integer(required=True)
    is_active = fields.Boolean(required=True)
    is_admin = fields.Boolean(required=True)
    email = fields.Text(required=True, default='')
    note = fields.Text(required=True, default='')

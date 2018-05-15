# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ApplicationUser(models.Model):
    _name = 'appserver.application_user'
    _table = 'application_user'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    user_id = fields.Many2one(string='User', required=True, comodel_name='appserver.user', ondelete='cascade')
    application_id = fields.Many2one(string='Application', required=True, comodel_name='appserver.application',
                                     ondelete='cascade')
    is_admin = fields.Boolean(required=True)

    _sql_constraints = [
        ('user_id_unique',
         'UNIQUE(user_id)',
         _(u'The user_id must be unique')),
        ('application_id_unique',
         'UNIQUE(application_id)',
         _(u'The application_id must be unique')),
    ]
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class OrganizationUser(models.Model):
    _name = 'appserver.organization_user'
    _table = 'organization_user'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    user_id = fields.Many2one(string='User', required=True, comodel_name='appserver.user', ondelete='cascade')
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization',
                                      ondelete='cascade')
    is_admin = fields.Boolean(required=True)

    _sql_constraints = [
        ('user_id_unique',
         'UNIQUE(user_id)',
         _(u'The user_id must be unique')),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         _(u'The organization_id must be unique')),
    ]

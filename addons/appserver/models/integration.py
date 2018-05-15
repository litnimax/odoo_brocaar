# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Integration(models.Model):
    _name = 'appserver.integration'
    _table = 'integration'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    application_id = fields.Many2one(string='Application', required=True, comodel_name='appserver.application',
                                     ondelete='cascade')
    kind = fields.Char(size=20, required=True)
    settings = fields.Text()

    _sql_constraints = [
        ('kind_unique',
         'UNIQUE(kind)',
         _(u'The kind must be unique')),
        ('application_id_unique',
         'UNIQUE(application_id)',
         _(u'The application_id must be unique')),
    ]

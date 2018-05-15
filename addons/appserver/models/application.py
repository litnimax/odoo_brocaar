# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Application(models.Model):
    _name = 'appserver.application'
    _table = 'application'
    _auto = False
    _rec_name = 'name'

    name = fields.Char(required=True)
    description = fields.Text(required=True)
    service_profile_id = fields.Char()
    service_profile_id_ = fields.Many2one(string='Service Profile', comodel_name='appserver.service_profile',
                                          compute='_get_service_profile_id', inverse='_set_service_profile')
    payload_codec = fields.Text(required=True, default='')
    payload_encoder_script = fields.Text(required=True, default='')
    payload_decoder_script = fields.Text(required=True, default='')
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization',
                                      ondelete='cascade')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         _(u'The name must be unique')),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         _(u'The organization_id must be unique')),
    ]

    @api.multi
    def _get_service_profile_id(self):
        for self in self:
            service_profile = self.env['appserver.service_profile'].search(
                [('service_profile_id', '=', self.service_profile_id)])
            if service_profile:
                self.service_profile_id_ = service_profile[0].id
            else:
                self.service_profile_id_ = False

    @api.multi
    def _set_service_profile(self):
        for self in self:
            sp = self.env['appserver.service_profile'].search([
                ('id','=', self.service_profile_id_.id)])
            if sp:
                self.service_profile_id = sp[0].service_profile_id
            else:
                self.service_profile_id = False
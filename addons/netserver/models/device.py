# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Device(models.Model):
    _name = 'netserver.device'
    _table = 'device'
    _rec_name = 'dev_eui'
    _auto = False
    _sql = """ALTER TABLE device ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS device_id_seq;
              ALTER TABLE device ALTER COLUMN id SET DEFAULT nextval('device_id_seq');
              UPDATE device SET id = nextval('device_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    dev_eui = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    service_profile_id = fields.Char()
    service_profile_id_ = fields.Many2one(string='Service Profile', required=True,
                                          comodel_name='netserver.service_profile', ondelete='cascade',
                                          compute='_get_service_profile_id')
    routing_profile_id = fields.Char()
    routing_profile_id_ = fields.Many2one(string='Routing Profile', required=True,
                                          comodel_name='netserver.routing_profile', ondelete='cascade',
                                          compute='_get_routing_profile_id')
    device_profile_id = fields.Char()
    device_profile_id_ = fields.Many2one(string='Device Profile', required=True,
                                         comodel_name='netserver.device_profile', ondelete='cascade',
                                         compute='_get_device_profile_id')
    skip_fcnt_check = fields.Boolean(required=True, default=False)

    @api.multi
    def _get_service_profile_id(self):
        for self in self:
            service_profile = self.env['netserver.service_profile'].search(
                [('service_profile_id', '=', self.service_profile_id)])
            if service_profile:
                self.service_profile_id_ = service_profile.id
            else:
                self.service_profile_id_ = False

    @api.multi
    def _get_routing_profile_id(self):
        for self in self:
            routing_profile = self.env['netserver.routing_profile'].search(
                [('routing_profile_id', '=', self.routing_profile_id)])
            if routing_profile:
                self.routing_profile_id_ = routing_profile.id
            else:
                self.routing_profile_id_ = False

    @api.multi
    def _get_device_profile_id(self):
        for self in self:
            device_profile = self.env['netserver.device_profile'].search(
                [('device_profile_id', '=', self.device_profile_id)])
            if device_profile:
                self.device_profile_id_ = device_profile.id
            else:
                self.device_profile_id_ = False
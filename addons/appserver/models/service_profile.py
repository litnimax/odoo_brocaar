# -*- coding: utf-8 -*-
import uuid
from odoo import models, fields, api, _


class ServiceProfile(models.Model):
    _name = 'appserver.service_profile'
    _table = 'service_profile'
    _auto = False
    _sql = """ALTER TABLE service_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS service_profile_id_seq;
              ALTER TABLE service_profile ALTER COLUMN id SET DEFAULT nextval('service_profile_id_seq');
              UPDATE service_profile SET id = nextval('service_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    service_profile_id = fields.Char(string='Service Profile ID', default=lambda x: uuid.uuid4())
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization')
    network_server_id = fields.Many2one(string='Network Server', required=True, comodel_name='appserver.network_server')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)

    @api.model
    def create(self, vals):
        vals['created_at'] = fields.Datetime.now()
        vals['updated_at'] = fields.Datetime.now()
        created = super(ServiceProfile, self).create(vals)
        return created

    @api.multi
    def write(self, vals):
        vals['updated_at'] = fields.Datetime.now()
        updated = super(ServiceProfile, self).write(vals)
        return updated
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RoutingProfile(models.Model):
    _name = 'netserver.routing_profile'
    _table = 'routing_profile'
    _rec_name = 'routing_profile_id'
    _auto = False
    _sql = """ALTER TABLE routing_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS routing_profile_id_seq;
              ALTER TABLE routing_profile ALTER COLUMN id SET DEFAULT nextval('routing_profile_id_seq');
              UPDATE routing_profile SET id = nextval('routing_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    routing_profile_id = fields.Char()
    as_id = fields.Char(size=255)
    ca_cert = fields.Text(required=True, default='')
    tls_cert = fields.Text(required=True, default='')
    tls_key = fields.Text(required=True, default='')
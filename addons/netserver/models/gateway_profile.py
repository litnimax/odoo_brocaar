# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GatewayProfile(models.Model):
    _name = 'netserver.gateway_profile'
    _table = 'gateway_profile'
    _rec_name = 'gateway_profile_id'
    _auto = False
    _sql = """ALTER TABLE gateway_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_profile_id_seq;
              ALTER TABLE gateway_profile ALTER COLUMN id SET DEFAULT nextval('gateway_profile_id_seq');
              UPDATE gateway_profile SET id = nextval('gateway_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    gateway_profile_id = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    channels = fields.Text(required=True)
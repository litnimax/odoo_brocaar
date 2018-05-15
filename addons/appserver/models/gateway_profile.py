# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GatewayProfile(models.Model):
    _name = 'appserver.gateway_profile'
    _table = 'gateway_profile'
    _auto = False
    _sql = """ALTER TABLE gateway_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_profile_id_seq;
              ALTER TABLE gateway_profile ALTER COLUMN id SET DEFAULT nextval('gateway_profile_id_seq');
              ALTER SEQUENCE gateway_profile_id_seq OWNER TO loraserver; 
              UPDATE gateway_profile SET id = nextval('gateway_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    name = fields.Char(size=100, required=True)
    gateway_profile_id = fields.Char()
    network_server_id = fields.Many2one(string='Network Server', required=True,
                                        comodel_name='appserver.network_server')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
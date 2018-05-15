# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DeviceProfile(models.Model):
    _name = 'appserver.device_profile'
    _table = 'device_profile'
    _auto = False
    _rec_name = 'name'
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    device_profile_id = fields.Char()
    network_server_id = fields.Many2one(string='Network Server', required=True, comodel_name='appserver.network_server',
                                        compute='_get_network_server_id')
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)

    @api.multi
    def _get_network_server_id(self):
        for self in self:
            network_server = self.env['appserver.network_server'].search(
                [('network_server_id', '=', self.network_server_id)])
            if network_server:
                self.network_server_id_ = network_server.id
            else:
                self.network_server_id_ = False

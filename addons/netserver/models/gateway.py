# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Gateway(models.Model):
    _name = 'netserver.gateway'
    _table = 'gateway'
    _rec_name = 'name'
    _auto = False
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              ALTER SEQUENCE gateway_id_seq OWNER TO loraserver; 
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    _sql_constraints = [
        (
            'gateway_name_key',
            'UNIQUE(name)',
            _(u'This name address is aloready used!')
        )
    ]

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    mac = fields.Char()
    name = fields.Char(size=100, required=True)
    description = fields.Text()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    first_seen_at = fields.Datetime()
    last_seen_at = fields.Datetime()
    location = fields.Char(required=True)
    altitude = fields.Float(required=True)
    channel_configuration_id = fields.Many2one(string='Channel Configuration', required=True,
                                               comodel_name='netserver.channel_configuration', ondelete='set null')
    gateway_profile_id = fields.Char()
    gateway_profile_id_ = fields.Many2one(string='Gateway Profile', comodel_name='netserver.gateway_profile',
                                          compute='_get_gateway_profile_id')

    @api.multi
    def _get_gateway_profile_id(self):
        for self in self:
            gateway_profile = self.env['netserver.gateway_profile'].search(
                [('gateway_profile_id', '=', self.device_profile_id)])
            if gateway_profile:
                self.gateway_profile_id_ = gateway_profile.id
            else:
                self.gateway_profile_id_ = False
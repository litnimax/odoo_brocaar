# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Device(models.Model):
    _name = 'appserver.device'
    _table = 'device'
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

    dev_eui = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    application_id = fields.Many2one(string='Application', required=True, comodel_name='appserver.application',
                                     ondelete='cascade')
    device_profile_id = fields.Char()
    device_profile_id_ = fields.Many2one(string='Device Profile', required=True, comodel='appserver.device_profile',
                                         ondelete='cascade', compute='_get_device_profile_id')
    name = fields.Char(size=100, required=True)
    description = fields.Text(required=True)
    last_seen_at = fields.Datetime(required=True)
    device_status_battery = fields.Integer(required=True)
    device_status_margin = fields.Integer(required=True)

    @api.multi
    def _get_device_profile_id(self):
        for self in self:
            device_profile = self.env['appserver.device_profile'].search(
                [('device_profile_id', '=', self.device_profile_id)])
            if device_profile:
                self.device_profile_id_ = device_profile.id
            else:
                self.device_profile_id_ = False


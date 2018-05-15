# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DeviceKeys(models.Model):
    _name = 'appserver.device_keys'
    _table = 'device_keys'
    _auto = False
    _sql = """ALTER TABLE device_keys ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS device_keys_id_seq;
              ALTER TABLE device_keys ALTER COLUMN id SET DEFAULT nextval('device_keys_id_seq');
              UPDATE device_keys SET id = nextval('device_keys_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(string='Device', required=True, comodel_name='appserver.device', ondelete='cascade',
                               compute='_get_device_id')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    app_key = fields.Binary(required=True)
    join_nonce = fields.Integer(required=True)

    @api.multi
    def _get_device_id(self):
        for self in self:
            dev_eui = self.env['appserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False

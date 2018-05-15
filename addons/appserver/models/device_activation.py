# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DeviceActivation(models.Model):
    _name = 'appserver.device_activation'
    _table = 'device_activation'
    _auto = False
    _sql = """ALTER TABLE device_activation ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS device_activation_id_seq;
              ALTER TABLE device_activation ALTER COLUMN id SET DEFAULT nextval('device_activation_id_seq');
              UPDATE device_activation SET id = nextval('device_activation_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    created_at = fields.Datetime(required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(string='Device', required=True, comodel_name='appserver.device', ondelete='cascade',
                               compute='_get_device_id')
    dev_addr = fields.Binary(required=True)
    app_s_key = fields.Binary(required=True)
    nwk_s_key = fields.Binary(required=True)

    @api.multi
    def _get_device_id(self):
        for self in self:
            dev_eui = self.env['appserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False

# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DeviceActivation(models.Model):
    _name = 'netserver.device_activation'
    _table = 'device_activation'
    _auto = False

    created_at = fields.Datetime(required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(string='Device', required=True, comodel_name='netserver.device', ondelete='cascade',
                               compute='_get_device_id')
    dev_addr = fields.Binary(required=True)
    nwk_s_key = fields.Binary(required=True)
    join_eui = fields.Binary(required=True)
    dev_nonce = fields.Binary(required=True)

    @api.multi
    def _get_device_id(self):
        for self in self:
            dev_eui = self.env['netserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False
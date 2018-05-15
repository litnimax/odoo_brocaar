# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DeviceQueue(models.Model):
    _name = 'appserver.device_queue'
    _table = 'device_queue'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    reference = fields.Char(size=100, required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(string='Device', required=True, comodel_name='appserver.device', ondelete='cascade',
                               compute='_get_device_id')
    confirmed = fields.Boolean(required=True, default=False)
    pending = fields.Boolean(required=True, default=False)
    fport = fields.Integer(required=True)
    data = fields.Binary(required=True)

    @api.multi
    def _get_device_id(self):
        for self in self:
            dev_eui = self.env['appserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False
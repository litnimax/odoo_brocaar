# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DeviceQueue(models.Model):
    _name = 'netserver.device_queue'
    _table = 'device_queue'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(string='Device', required=True, comodel_name='netserver.device', ondelete='cascade',
                               compute='_get_device_id')
    confirmed = fields.Boolean(required=True)
    frm_payload = fields.Char()
    f_cnt = fields.Integer(required=True)
    f_port = fields.Integer(required=True)
    is_pending = fields.Boolean(required=True)
    emit_at_time_since_gps_epoch = fields.Integer()
    timeout_after = fields.Datetime(required=True)

    @api.multi
    def _get_device_id(self):
        for self in self:
            dev_eui = self.env['netserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False
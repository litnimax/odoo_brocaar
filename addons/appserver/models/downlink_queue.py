# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DownlinkQueue(models.Model):
    _name = 'appserver.downlink_queue'
    _table = 'downlink_queue'
    _auto = False

    reference = fields.Char(size=100, required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(string='Node', required=True, comodel_name='appserver.node', ondelete='cascade',
                               compute='_get_node_id')
    confirmed = fields.Boolean(required=True, default=False)
    pending = fields.Boolean(required=True, default=False)
    fport = fields.Integer(required=True)
    data = fields.Binary(required=True)

    @api.multi
    def _get_node_id(self):
        for self in self:
            node = self.env['appserver.node'].search(
                [('dev_eui', '=', self.dev_eui)])
            if node:
                self.dev_eui_ = node.id
            else:
                self.dev_eui_ = False
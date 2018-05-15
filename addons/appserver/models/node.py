# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Node(models.Model):
    _name = 'appserver.node'
    _table = 'node'
    _auto = False
    _rec_name = 'name'
    _sql = """ALTER TABLE node ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS node_id_seq;
              ALTER TABLE node ALTER COLUMN id SET DEFAULT nextval('node_id_seq');
              UPDATE node SET id = nextval('node_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    name = fields.Char(size=100, required=True, default='')
    description = fields.Text(required=True)
    application_id = fields.Many2one(string='Application', required=True, comodel_name='appserver.application',
                                     ondelete='cascade')
    dev_eui = fields.Char()
    app_eui = fields.Char()
    is_abp = fields.Boolean(required=True, default=False)
    app_key = fields.Binary(required=True)
    used_dev_nonces = fields.Char()
    rx_delay = fields.Integer(required=True)
    rx1_dr_offset = fields.Integer(required=True)
    relax_fcnt = fields.Boolean(required=True, default=False)
    is_class_c = fields.Boolean(required=True, default=False)
    rx_window = fields.Integer(required=True, default=0)
    rx2_dr = fields.Integer(required=True, default=0)
    app_s_key = fields.Binary(required=True, default=b'\\x00000000000000000000000000000000')
    nwk_s_key = fields.Binary(required=True, default=b'\\x00000000000000000000000000000000')
    dev_addr = fields.Binary(required=True, default=b'\\x00000000')
    adr_interval = fields.Integer(required=True, default=0)
    installation_margin = fields.Float(digits=(5, 2), required=True, default=0)
    use_application_settings = fields.Boolean(required=True, default=False)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         _(u'The name must be unique')),
        ('application_id_unique',
         'UNIQUE(application_id)',
         _(u'The application_id must be unique')),
    ]
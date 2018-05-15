# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _


logger = logging.getLogger(__name__)


class Gateway(models.Model):
    _name = 'appserver.gateway'
    _table = 'gateway'
    _auto = False
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              ALTER SEQUENCE gateway_id_seq OWNER TO loraserver; 
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    def _check_removed_columns(self, log=False):
        # Override not to remove columns
        pass


    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    mac = fields.Char(string='MAC Address', compute='_get_mac', inverse='_set_mac')
    name = fields.Char(size=100, required=True)
    description = fields.Text()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization',
                                      ondelete='cascade')
    ping = fields.Boolean(required=True, default=False)
    last_ping_id = fields.Many2one(string='Gateway Ping', comodel_name='appserver.gateway_ping', ondelete='set null')
    last_ping_sent_at = fields.Datetime(required=True)
    network_server_id = fields.Many2one(string='Network Server', comodel_name='appserver.network_server',
                                        ondelete='set null')

    """
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         _(u'The name must be unique')),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         _(u'The organization_id must be unique')),
    ]
    """


    @api.multi
    def _get_mac(self):
        for self in self:
            cr = self._cr
            res = cr.execute(
                'SELECT CAST (mac AS VARCHAR) AS mac FROM gateway WHERE '
                'id = {}'.format(self.id)
            )
            mac = cr.fetchall()
            logger.info('11111 {}'.format(mac))
            self.mac = mac[0][0] if mac else False


    @api.multi
    def _set_mac(self):
        for self in self:
            cr = self._cr
            # TODO: add @api.constrains('mac') to check address
            # TODO: Be sure that CAST works - check how loraserver can see "our" mac
            cr.execute(
                "UPDATE gateway SET mac =  CAST ('{}' AS BYTEA) WHERE "
                "id = {}".format(self.mac, self.id)
            )




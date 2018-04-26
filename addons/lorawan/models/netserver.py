from odoo import models, fields, api


class Gateway(models.Model):
    _name = 'lorawan.gateway'

    mac = fields.Binary()
    name = fields.Char(size=100, required=True)
    description = fields.Text()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    first_seen_at = fields.Datetime()
    last_seen_at = fields.Datetime()
    # TODO location field must be point type
    location = fields.Char()
    altitude = fields.Float()

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The name must be unique"),
        ('mac_unique',
         'UNIQUE(mac)',
         "The mac must be unique"),
    ]


class GatewayStats(models.Model):
    _name = 'lorawan.gateway_stats'

    mac = fields.Many2one(required=True, comodel_name='lorawan.gateway', ondelete='cascade')
    timestamp = fields.Datetime(required=True)
    interval = fields.Char(size=10, required=True)
    rx_packets_received = fields.Integer(required=True)
    rx_packets_received_ok = fields.Integer(required=True)
    tx_packets_received = fields.Integer(required=True)
    tx_packets_emitted = fields.Integer(required=True)

    _sql_constraints = [
        ('mac_unique',
         'UNIQUE(mac)',
         "The mac must be unique"),
        ('timestamp_unique',
         'UNIQUE(timestamp)',
         "The timestamp must be unique"),
        ('interval_unique',
         'UNIQUE(interval)',
         "The interval must be unique"),
    ]


class FrameLog(models.Model):
    _name = 'lorawan.frame_log'

    created_at = fields.Datetime(required=True)
    dev_eui = fields.Binary(required=True)
    # TODO rx_info_set and tx_info must have jsonb type
    rx_info_set = fields.Text()
    tx_info = fields.Text()
    phy_payload = fields.Binary(required=True)



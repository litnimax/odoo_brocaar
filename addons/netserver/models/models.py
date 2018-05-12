# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Gateway(models.Model):
    _name = 'netserver.gateway'
    _table = 'gateway'
    _rec_name = 'name'
    _auto = False
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    _sql_constraints = [
        (
            'gateway_name_key',
            'UNIQUE(name)',
            _(u'This name address is aloready used!')
        )
    ]

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    mac = fields.Char()
    name = fields.Char(size=100, required=True)
    description = fields.Text()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    first_seen_at = fields.Datetime()
    last_seen_at = fields.Datetime()
    location = fields.Char(required=True)
    altitude = fields.Float(required=True)
    channel_configuration_id = fields.Many2one(required=True,
                                               comodel_name='netserver.channel_configuration',
                                               ondelete='set null')
    gateway_profile_id = fields.Char()
    gateway_profile_id_ = fields.Many2one(string='Gateway Profile',
                                         comodel_name='netserver.gateway_profile',
                                         compute='_get_gateway_profile_id')

    @api.multi
    def _get_gateway_profile_id(self):
        for self in self:
            gateway_profile = self.env['netserver.gateway_profile'].search(
                [('gateway_profile_id', '=', self.device_profile_id)])
            if gateway_profile:
                self.gateway_profile_id_ = gateway_profile.id
            else:
                self.gateway_profile_id_ = False


class GatewayStats(models.Model):
    _name = 'netserver.gateway_stats'
    _table = 'gateway_stats'
    _auto = False

    mac = fields.Char()
    mac_ = fields.Many2one(required=True,
                           string='Gateway Profile',
                           comodel_name='netserver.gateway',
                           compute='_get_mac',
                           ondelete='cascade')
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

    @api.multi
    def _get_mac(self):
        for self in self:
            mac = self.env['netserver.gateway'].search(
                [('mac', '=', self.mac)])
            if mac:
                self.mac_ = mac.id
            else:
                self.mac_ = False


class FrameLog(models.Model):
    _name = 'netserver.frame_log'
    _table = 'frame_log'
    _auto = False

    created_at = fields.Datetime(required=True)
    dev_eui = fields.Char(required=True)
    rx_info_set = fields.Text()
    tx_info = fields.Text()
    phy_payload = fields.Binary(required=True)


class ChannelConfiguration(models.Model):
    _name = 'netserver.channel_configuration'
    _table = 'channel_configuration'
    _auto = False

    name = fields.Char(size=100, required=True)
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    band = fields.Char(size=20, required=True)
    channels = fields.Integer(required=True)


class ExtraChannel(models.Model):
    _name = 'netserver.extra_channel'
    _table = 'extra_channel'
    _auto = False

    channel_configuration_id = fields.Many2one(required=True, comodel_name='netserver.channel_configuration',
                                               ondelete='cascade')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    modulation = fields.Char(size=10, required=True)
    frequency = fields.Integer(required=True)
    bandwidth = fields.Integer(required=True)
    bit_rate = fields.Integer(required=True)
    spread_factors = fields.Integer()


class DeviceProfile(models.Model):
    _name = 'netserver.device_profile'
    _table = 'device_profile'
    _rec_name = 'device_profile_id'
    _auto = False
    _sql = """ALTER TABLE device_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS device_profile_id_seq;
              ALTER TABLE device_profile ALTER COLUMN id SET DEFAULT nextval('device_profile_id_seq');
              UPDATE device_profile SET id = nextval('device_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    device_profile_id = fields.Char()
    supports_class_b = fields.Boolean(required=True)
    class_b_timeout = fields.Integer(required=True)
    ping_slot_period = fields.Integer(required=True)
    ping_slot_dr = fields.Integer(required=True)
    ping_slot_freq = fields.Integer(required=True)
    supports_class_c = fields.Boolean(required=True)
    class_c_timeout = fields.Integer(required=True)
    mac_version = fields.Char(size=10, required=True)
    reg_params_revision = fields.Char(size=10, required=True)
    rx_delay_1 = fields.Integer(required=True)
    rx_dr_offset_1 = fields.Integer(required=True)
    rx_data_rate_2 = fields.Integer(required=True)
    rx_freq_2 = fields.Integer(required=True)
    factory_preset_freqs = fields.Integer()
    max_eirp = fields.Integer(required=True)
    max_duty_cycle = fields.Integer(required=True)
    supports_join = fields.Boolean(required=True)
    rf_region = fields.Char(size=20, required=True)
    supports_32bit_fcnt = fields.Boolean(required=True)


class ServiceProfile(models.Model):
    _name = 'netserver.service_profile'
    _table = 'service_profile'
    _rec_name = 'service_profile_id'
    _auto = False
    _sql = """ALTER TABLE service_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS service_profile_id_seq;
              ALTER TABLE service_profile ALTER COLUMN id SET DEFAULT nextval('service_profile_id_seq');
              UPDATE service_profile SET id = nextval('service_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    service_profile_id = fields.Char()
    ul_rate = fields.Integer(required=True)
    ul_bucket_size = fields.Integer(required=True)
    ul_rate_policy = fields.Char(size=4, required=True)
    dl_rate = fields.Integer(required=True)
    dl_bucket_size = fields.Integer(required=True)
    dl_rate_policy = fields.Char(size=4, required=True)
    add_gw_metadata = fields.Boolean(required=True)
    dev_status_req_freq = fields.Integer(required=True)
    report_dev_status_battery = fields.Boolean(required=True)
    report_dev_status_margin = fields.Boolean(required=True)
    dr_min = fields.Integer(required=True)
    dr_max = fields.Integer(required=True)
    channel_mask = fields.Char()
    pr_allowed = fields.Boolean(required=True)
    hr_allowed = fields.Boolean(required=True)
    ra_allowed = fields.Boolean(required=True)
    nwk_geo_loc = fields.Boolean(required=True)
    target_per = fields.Integer(required=True)
    min_gw_diversity = fields.Integer(required=True)


class RoutingProfile(models.Model):
    _name = 'netserver.routing_profile'
    _table = 'routing_profile'
    _rec_name = 'routing_profile_id'
    _auto = False
    _sql = """ALTER TABLE routing_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS routing_profile_id_seq;
              ALTER TABLE routing_profile ALTER COLUMN id SET DEFAULT nextval('routing_profile_id_seq');
              UPDATE routing_profile SET id = nextval('routing_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    routing_profile_id = fields.Char()
    as_id = fields.Char(size=255)
    ca_cert = fields.Text(required=True, default='')
    tls_cert = fields.Text(required=True, default='')
    tls_key = fields.Text(required=True, default='')


class Device(models.Model):
    _name = 'netserver.device'
    _table = 'device'
    _rec_name = 'dev_eui'
    _auto = False
    _sql = """ALTER TABLE device ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS device_id_seq;
              ALTER TABLE device ALTER COLUMN id SET DEFAULT nextval('device_id_seq');
              UPDATE device SET id = nextval('device_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    dev_eui = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    service_profile_id = fields.Char()
    service_profile_id_ = fields.Many2one(required=True,
                                          string='Service Profile',
                                          comodel_name='netserver.service_profile',
                                          compute='_get_service_profile_id',
                                          ondelete='cascade')
    routing_profile_id = fields.Char()
    routing_profile_id_ = fields.Many2one(required=True,
                                          string='Routing Profile',
                                          comodel_name='netserver.routing_profile',
                                          compute='_get_routing_profile_id',
                                          ondelete='cascade')
    device_profile_id = fields.Char()
    device_profile_id_ = fields.Many2one(required=True,
                                         string='Device Profile',
                                         comodel_name='netserver.device_profile',
                                         compute='_get_device_profile_id',
                                         ondelete='cascade')
    skip_fcnt_check = fields.Boolean(required=True, default=False)

    @api.multi
    def _get_service_profile_id(self):
        for self in self:
            service_profile = self.env['netserver.service_profile'].search(
                [('service_profile_id', '=', self.service_profile_id)])
            if service_profile:
                self.service_profile_id_ = service_profile.id
            else:
                self.service_profile_id_ = False

    @api.multi
    def _get_routing_profile_id(self):
        for self in self:
            routing_profile = self.env['netserver.routing_profile'].search(
                [('routing_profile_id', '=', self.routing_profile_id)])
            if routing_profile:
                self.routing_profile_id_ = routing_profile.id
            else:
                self.routing_profile_id_ = False

    @api.multi
    def _get_device_profile_id(self):
        for self in self:
            device_profile = self.env['netserver.device_profile'].search(
                [('device_profile_id', '=', self.device_profile_id)])
            if device_profile:
                self.device_profile_id_ = device_profile.id
            else:
                self.device_profile_id_ = False


class DeviceActivation(models.Model):
    _name = 'netserver.device_activation'
    _table = 'device_activation'
    _auto = False

    created_at = fields.Datetime(required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(required=True,
                               string='Device EUI',
                               comodel_name='netserver.device',
                               compute='_get_dev_eui',
                               ondelete='cascade')
    dev_addr = fields.Binary(required=True)
    nwk_s_key = fields.Binary(required=True)
    join_eui = fields.Binary(required=True)
    dev_nonce = fields.Binary(required=True)

    @api.multi
    def _get_dev_eui(self):
        for self in self:
            dev_eui = self.env['netserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False


class DeviceQueue(models.Model):
    _name = 'netserver.device_queue'
    _table = 'device_queue'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(required=True,
                               string='Device EUI',
                               comodel_name='netserver.device',
                               compute='_get_dev_eui',
                               ondelete='cascade')
    confirmed = fields.Boolean(required=True)
    frm_payload = fields.Char()
    f_cnt = fields.Integer(required=True)
    f_port = fields.Integer(required=True)
    is_pending = fields.Boolean(required=True)
    emit_at_time_since_gps_epoch = fields.Integer()
    timeout_after = fields.Datetime(required=True)

    @api.multi
    def _get_dev_eui(self):
        for self in self:
            dev_eui = self.env['netserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False


class GatewayProfile(models.Model):
    _name = 'netserver.gateway_profile'
    _table = 'gateway_profile'
    _rec_name = 'gateway_profile_id'
    _auto = False
    _sql = """ALTER TABLE gateway_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_profile_id_seq;
              ALTER TABLE gateway_profile ALTER COLUMN id SET DEFAULT nextval('gateway_profile_id_seq');
              UPDATE gateway_profile SET id = nextval('gateway_profile_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    gateway_profile_id = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    channels = fields.Text(required=True)


class GatewayProfileExtraChannel(models.Model):
    _name = 'netserver.gateway_profile_extra_channel'
    _table = 'gateway_profile_extra_channel'
    _auto = False

    gateway_profile_id = fields.Char()
    gateway_profile_id_ = fields.Many2one(required=True,
                                          string='Gateway Profile',
                                          comodel_name='netserver.gateway_profile',
                                          compute='_get_gateway_profile_id',
                                          ondelete='cascade')
    modulation = fields.Char(size=10, required=True)
    frequency = fields.Integer(required=True)
    bandwidth = fields.Integer(required=True)
    bitrate = fields.Integer(required=True)
    spreading_factors = fields.Text()

    @api.multi
    def _get_gateway_profile_id(self):
        for self in self:
            gateway_profile = self.env['netserver.gateway_profile'].search(
                [('gateway_profile_id', '=', self.device_profile_id)])
            if gateway_profile:
                self.gateway_profile_id_ = gateway_profile.id
            else:
                self.gateway_profile_id_ = False

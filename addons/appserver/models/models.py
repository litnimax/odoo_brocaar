# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Application(models.Model):
    _name = 'appserver.application'
    _table = 'application'
    _auto = False
    _rec_name = 'name'

    name = fields.Char(required=True)
    description = fields.Text(required=True)
    service_profile_id = fields.Char()
    service_profile_id_ = fields.Many2one(string='Service Profile', comodel_name='appserver.service_profile',
                                          compute='_get_service_profile_id', inverse='_set_service_profile')
    payload_codec = fields.Text(required=True, default='')
    payload_encoder_script = fields.Text(required=True, default='')
    payload_decoder_script = fields.Text(required=True, default='')
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization',
                                      ondelete='cascade')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         _(u'The name must be unique')),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         _(u'The organization_id must be unique')),
    ]

    @api.multi
    def _get_service_profile_id(self):
        for self in self:
            service_profile = self.env['appserver.service_profile'].search(
                [('service_profile_id', '=', self.service_profile_id)])
            if service_profile:
                self.service_profile_id_ = service_profile[0].id
            else:
                self.service_profile_id_ = False

    @api.multi
    def _set_service_profile(self):
        for self in self:
            sp = self.env['appserver.service_profile'].search([
                ('id','=', self.service_profile_id_.id)])
            if sp:
                self.service_profile_id = sp[0].service_profile_id
            else:
                self.service_profile_id = False


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


class User(models.Model):
    _name = 'appserver.user'
    _table = 'user'
    _auto = False
    _rec_name = 'username'

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    username = fields.Char(size=100, required=True)
    password_hash = fields.Char(size=200, required=True)
    session_ttl = fields.Integer(required=True)
    is_active = fields.Boolean(required=True)
    is_admin = fields.Boolean(required=True)
    email = fields.Text(required=True, default='')
    note = fields.Text(required=True, default='')


class ApplicationUser(models.Model):
    _name = 'appserver.application_user'
    _table = 'application_user'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    user_id = fields.Many2one(string='User', required=True, comodel_name='appserver.user', ondelete='cascade')
    application_id = fields.Many2one(string='Application', required=True, comodel_name='appserver.application',
                                     ondelete='cascade')
    is_admin = fields.Boolean(required=True)

    _sql_constraints = [
        ('user_id_unique',
         'UNIQUE(user_id)',
         _(u'The user_id must be unique')),
        ('application_id_unique',
         'UNIQUE(application_id)',
         _(u'The application_id must be unique')),
    ]


class Organization(models.Model):
    _name = 'appserver.organization'
    _table = 'organization'
    _auto = False
    _rec_name = 'name'

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)
    display_name = fields.Char(size=100, required=True)
    can_have_gateways = fields.Boolean(required=True)


class OrganizationUser(models.Model):
    _name = 'appserver.organization_user'
    _table = 'organization_user'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    user_id = fields.Many2one(string='User', required=True, comodel_name='appserver.user', ondelete='cascade')
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization',
                                      ondelete='cascade')
    is_admin = fields.Boolean(required=True)

    _sql_constraints = [
        ('user_id_unique',
         'UNIQUE(user_id)',
         _(u'The user_id must be unique')),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         _(u'The organization_id must be unique')),
    ]


class Gateway(models.Model):
    _name = 'appserver.gateway'
    _table = 'gateway'
    _auto = False
    _rec_name = 'name'
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    mac = fields.Char()
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

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         _(u'The name must be unique')),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         _(u'The organization_id must be unique')),
    ]


class Integration(models.Model):
    _name = 'appserver.integration'
    _table = 'integration'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    application_id = fields.Many2one(string='Application', required=True, comodel_name='appserver.application',
                                     ondelete='cascade')
    kind = fields.Char(size=20, required=True)
    settings = fields.Text()

    _sql_constraints = [
        ('kind_unique',
         'UNIQUE(kind)',
         _(u'The kind must be unique')),
        ('application_id_unique',
         'UNIQUE(application_id)',
         _(u'The application_id must be unique')),
    ]


class GatewayPing(models.Model):
    _name = 'appserver.gateway_ping'
    _table = 'gateway_ping'
    _auto = False
    _rec_name = 'dr'

    created_at = fields.Datetime(required=True)
    # TODO gateway_mac must be defined as indicated below
    gateway_mac = fields.Char()
    gateway_mac_ = fields.Many2one(string='Gateway', required=True, comodel_name='appserver.gateway',
                                   ondelete='cascade', compute='_get_gateway_id')
    frequency = fields.Integer(required=True)
    dr = fields.Integer(required=True)

    @api.multi
    def _get_gateway_id(self):
        for self in self:
            mac = self.env['appserver.gateway'].search(
                [('mac', '=', self.gateway_mac)])
            if mac:
                self.gateway_mac_ = mac.id
            else:
                self.gateway_mac_ = False


class GatewayPingRx(models.Model):
    _name = 'appserver.gateway_ping_rx'
    _table = 'gateway_ping_rx'
    _auto = False

    created_at = fields.Datetime(required=True)
    ping_id = fields.Many2one(string='Gateway Ping', required=True, comodel_name='appserver.gateway_ping',
                              ondelete='cascade')
    # TODO gateway_mac must be defined as indicated below
    gateway_mac = fields.Char()
    gateway_mac_ = fields.Many2one(string='Gateway', required=True, comodel_name='appserver.gateway',
                                   ondelete='cascade', compute='_get_gateway_id')
    received_at = fields.Datetime(required=True)
    rssi = fields.Integer(required=True)
    lora_snr = fields.Float(digits=(3, 1), required=True)
    location = fields.Char()
    altitude = fields.Float()

    @api.multi
    def _get_gateway_id(self):
        for self in self:
            mac = self.env['appserver.gateway'].search(
                [('mac', '=', self.gateway_mac)])
            if mac:
                self.gateway_mac_ = mac.id
            else:
                self.gateway_mac_ = False


class NetworkServer(models.Model):
    _name = 'appserver.network_server'
    _table = 'network_server'
    _auto = False
    _rec_name = 'name'

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)
    server = fields.Char(size=255, required=True)
    ca_cert = fields.Text(required=True, default='')
    tls_cert = fields.Text(required=True, default='')
    tls_key = fields.Text(required=True, default='')
    routing_profile_ca_cert = fields.Text(required=True, default='')
    routing_profile_tls_cert = fields.Text(required=True, default='')
    routing_profile_tls_key = fields.Text(required=True, default='')
    gateway_discovery_enabled = fields.Boolean(required=True, default=False)
    gateway_discovery_interval = fields.Integer(required=True, default=0)
    gateway_discovery_tx_frequency = fields.Integer(required=True, default=0)
    gateway_discovery_dr = fields.Integer(required=True, default=0)


class ServiceProfile(models.Model):
    _name = 'appserver.service_profile'
    _table = 'service_profile'
    _auto = False
<<<<<<< HEAD
    _rec_name = 'name'
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)
=======
    _sql = """ALTER TABLE service_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS service_profile_id_seq;
              ALTER TABLE service_profile ALTER COLUMN id SET DEFAULT nextval('service_profile_id_seq');
              UPDATE service_profile SET id = nextval('service_profile_id_seq');
    """


    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

>>>>>>> 455097c3c35de7bbc0354bc86c4d03f4e75598a8

    # TODO service_profile_id must be primary key with uuid type
    service_profile_id = fields.Char()
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization')
    network_server_id = fields.Many2one(string='Network Server', required=True, comodel_name='appserver.network_server')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)


class DeviceProfile(models.Model):
    _name = 'appserver.device_profile'
    _table = 'device_profile'
    _auto = False
    _rec_name = 'name'
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    device_profile_id = fields.Char()
    network_server_id = fields.Many2one(string='Network Server', required=True, comodel_name='appserver.network_server',
                                        compute='_get_network_server_id')
    organization_id = fields.Many2one(string='Organization', required=True, comodel_name='appserver.organization')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)

    @api.multi
    def _get_network_server_id(self):
        for self in self:
            network_server = self.env['appserver.network_server'].search(
                [('network_server_id', '=', self.network_server_id)])
            if network_server:
                self.network_server_id_ = network_server.id
            else:
                self.network_server_id_ = False


class Device(models.Model):
    _name = 'appserver.device'
    _table = 'device'
    _auto = False
    _rec_name = 'name'
    _sql = """ALTER TABLE gateway ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS gateway_id_seq;
              ALTER TABLE gateway ALTER COLUMN id SET DEFAULT nextval('gateway_id_seq');
              UPDATE gateway SET id = nextval('gateway_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    dev_eui = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    application_id = fields.Many2one(string='Application', required=True, comodel_name='appserver.application',
                                     ondelete='cascade')
    device_profile_id = fields.Char()
    device_profile_id_ = fields.Many2one(string='Device Profile', required=True, comodel='appserver.device_profile',
                                         ondelete='cascade', compute='_get_device_profile_id')
    name = fields.Char(size=100, required=True)
    description = fields.Text(required=True)
    last_seen_at = fields.Datetime(required=True)
    device_status_battery = fields.Integer(required=True)
    device_status_margin = fields.Integer(required=True)

    @api.multi
    def _get_device_profile_id(self):
        for self in self:
            device_profile = self.env['appserver.device_profile'].search(
                [('device_profile_id', '=', self.device_profile_id)])
            if device_profile:
                self.device_profile_id_ = device_profile.id
            else:
                self.device_profile_id_ = False


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


class DeviceQueueMapping(models.Model):
    _name = 'appserver.device_queue_mapping'
    _table = 'device_queue_mapping'
    _auto = False

    created_at = fields.Datetime(required=True)
    reference = fields.Text(required=True)
    dev_eui = fields.Char()
    dev_eui_ = fields.Many2one(string='Device', required=True, comodel_name='appserver.device', ondelete='cascade',
                               compute='_get_device_id')
    f_cnt = fields.Integer(required=True)

    @api.multi
    def _get_device_id(self):
        for self in self:
            dev_eui = self.env['appserver.device'].search(
                [('dev_eui', '=', self.dev_eui)])
            if dev_eui:
                self.dev_eui_ = dev_eui.id
            else:
                self.dev_eui_ = False


class GatewayProfile(models.Model):
    _name = 'appserver.gateway_profile'
    _table = 'gateway_profile'
    _auto = False
    _rec_name = 'name'
    _sql = """ALTER TABLE device_activation ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS device_activation_id_seq;
              ALTER TABLE device_activation ALTER COLUMN id SET DEFAULT nextval('device_activation_id_seq');
              UPDATE device_activation SET id = nextval('device_activation_id_seq');
    """

    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)

    gateway_profile_id = fields.Char()
    network_server_id = fields.Many2one(string='Network Server', required=True, comodel_name='appserver.network_server')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)

# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Application(models.Model):
    _name = 'appserver.application'
    _table = 'application'
    _auto = False

    name = fields.Char(required=True)
    description = fields.Text(required=True)
    # TODO device_profile_id must be defined as indicated below and must have uuid type
    # service_profile_id = fields.Many2one(comodel_name='appserver.service_profile')
    service_profile_id_ = fields.Many2one('appserver.service_profile',
                                          compute='_get_service_profile',
                                          inverse='_set_service_profile')
    service_profile_id = fields.Char()
    payload_codec = fields.Text(required=True, default='')
    payload_encoder_script = fields.Text(required=True, default='')
    payload_decoder_script = fields.Text(required=True, default='')
    organization_id = fields.Many2one(required=True, comodel_name='appserver.organization', ondelete='cascade')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The name must be unique"),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         "The organization_id must be unique"),
    ]


    @api.multi
    def _get_service_profile(self):
        for self in self:
            sp = self.env['appserver.service_profile'].search([
                ('service_profile_id','=', self.service_profile_id)])
            if sp:
                self.service_profile_id_ = sp[0].id
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

    name = fields.Char(size=100, required=True, default='')
    description = fields.Text(required=True)
    application_id = fields.Many2one(required=True, comodel_name='appserver.application', ondelete='cascade')
    # TODO dev_eui must be primary key
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
    installation_margin = fields.Float(digits=(5,2), required=True, default=0)
    use_application_settings = fields.Boolean(required=True, default=False)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The name must be unique"),
        ('application_id_unique',
         'UNIQUE(application_id)',
         "The application_id must be unique"),
    ]

class DownlinkQueue(models.Model):
    _name = 'appserver.downlink_queue'
    _table = 'downlink_queue'
    _auto = False

    reference = fields.Char(size=100, required=True)
    # TODO dev_eui must be defined as indicated below
    # dev_eui = fields.Many2one(required=True, comodel_name='appserver.node', ondelete='cascade')
    dev_eui = fields.Char()
    confirmed = fields.Boolean(required=True, default=False)
    pending = fields.Boolean(required=True, default=False)
    fport = fields.Integer(required=True)
    data = fields.Binary(required=True)

class User(models.Model):
    _name = 'appserver.user'
    _table = 'user'
    _auto = False

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
    user_id = fields.Many2one(required=True, comodel_name='appserver.user', ondelete='cascade')
    application_id = fields.Many2one(required=True, comodel_name='appserver.application', ondelete='cascade')
    is_admin = fields.Boolean(required=True)

    _sql_constraints = [
        ('user_id_unique',
         'UNIQUE(user_id)',
         "The user_id must be unique"),
        ('application_id_unique',
         'UNIQUE(application_id)',
         "The application_id must be unique"),
    ]

class Organization(models.Model):
    _name = 'appserver.organization'
    _table = 'organization'
    _auto = False

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
    user_id = fields.Many2one(required=True, comodel_name='appserver.user', ondelete='cascade')
    organization_id = fields.Many2one(required=True, comodel_name='appserver.organization', ondelete='cascade')
    is_admin = fields.Boolean(required=True)

    _sql_constraints = [
        ('user_id_unique',
         'UNIQUE(user_id)',
         "The user_id must be unique"),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         "The organization_id must be unique"),
    ]

class Gateway(models.Model):
    _name = 'appserver.gateway'
    _table = 'gateway'
    _auto = False

    # TODO mac sut be primarykey
    mac = fields.Char()
    name = fields.Char(size=100, required=True)
    description = fields.Text()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    organization_id = fields.Many2one(required=True, comodel_name='appserver.organization', ondelete='cascade')
    ping = fields.Boolean(required=True, default=False)
    last_ping_id = fields.Many2one(comodel_name='appserver.gateway_ping', ondelete='set null')
    last_ping_sent_at = fields.Datetime(required=True)
    network_server_id = fields.Many2one(comodel_name='appserver.network_server', ondelete='set null')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The name must be unique"),
        ('organization_id_unique',
         'UNIQUE(organization_id)',
         "The organization_id must be unique"),
    ]

class Integration(models.Model):
    _name = 'appserver.integration'
    _table = 'integration'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    application_id = fields.Many2one(required=True, comodel_name='appserver.application', ondelete='cascade')
    kind = fields.Char(size=20, required=True)
    # TODO settings must have jsonb type
    settings = fields.Text()

    _sql_constraints = [
        ('kind_unique',
         'UNIQUE(kind)',
         "The kind must be unique"),
        ('application_id_unique',
         'UNIQUE(application_id)',
         "The application_id must be unique"),
    ]

class GatewayPing(models.Model):
    _name = 'appserver.gateway_ping'
    _table = 'gateway_ping'
    _auto = False

    created_at = fields.Datetime(required=True)
    # TODO gateway_mac must be defined as indicated below
    # gateway_mac = fields.Many2one(required=True, comodel_name='appserver.gateway', ondelete='cascade')
    gateway_mac = fields.Char()
    frequency = fields.Integer(required=True)
    dr = fields.Integer(required=True)

class GatewayPingRx(models.Model):
    _name = 'appserver.gateway_ping_rx'
    _table = 'gateway_ping_rx'
    _auto = False

    created_at = fields.Datetime(required=True)
    ping_id = fields.Many2one(required=True, comodel_name='appserver.gateway_ping', ondelete='cascade')
    # TODO gateway_mac must be defined as indicated below
    # gateway_mac = fields.Many2one(required=True, comodel_name='appserver.gateway', ondelete='cascade')
    gateway_mac = fields.Char()
    received_at = fields.Datetime(required=True)
    rssi = fields.Integer(required=True)
    lora_snr = fields.Float(digits=(3,1), required=True)
    # TODO location field must be point type
    location = fields.Char()
    altitude = fields.Float()

class NetworkServer(models.Model):
    _name = 'appserver.network_server'
    _table = 'network_server'
    _auto = False

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
    _sql = """ALTER TABLE service_profile ADD COLUMN IF NOT EXISTS id INTEGER;
              CREATE SEQUENCE IF NOT EXISTS service_profile_id_seq;
              ALTER TABLE service_profile ALTER COLUMN id SET DEFAULT nextval('service_profile_id_seq');
              UPDATE service_profile SET id = nextval('service_profile_id_seq');
    """


    @api.model_cr
    def init(self):
        self.env.cr.execute(self._sql)


    # TODO service_profile_id must be primary key with uuid type
    service_profile_id = fields.Char()
    organization_id = fields.Many2one(required=True, comodel_name='appserver.organization')
    network_server_id = fields.Many2one(required=True, comodel_name='appserver.network_server')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)

class DeviceProfile(models.Model):
    _name = 'appserver.device_profile'
    _table = 'device_profile'
    _auto = False

    # TODO device_profile_id must be primary key with uuid type
    device_profile_id = fields.Char()
    network_server_id = fields.Many2one(required=True, comodel_name='appserver.network_server')
    organization_id  = fields.Many2one(required=True, comodel_name='appserver.organization')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)



class Device(models.Model):
    _name = 'appserver.device'
    _table = 'device'
    _auto = False

    # TODO dev_eui must be primary key
    dev_eui = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    application_id = fields.Many2one(required=True, comodel_name='appserver.application', ondelete='cascade')
    # TODO device_profile_id must be defined as indicated below
    # device_profile_id = fields.Many2one(required=True, comodel_name='appserver.device_profile', ondelete='cascade')
    device_profile_id = fields.Char()
    device_profile_id_ = fields.Many2one(string='Device Profile',
                                         comodel='appserver.device_profile', 
                                         compute='_get_device_profile_id',
                                         ondelete='cascade')
    name = fields.Char(size=100, required=True)
    description = fields.Text(required=True)
    last_seen_at = fields.Datetime(required=True)
    device_status_battery = fields.Integer(required=True)
    device_status_margin = fields.Integer(required=True)


    @api.multi
    def _get_device_profile_id(self):
        for self in self:
            device_profile = self.env['appserver.device_profile'].search(
                            [('device_profile_id','=', self.device_profile_id)])
            if device_profile:
                self.device_profile_id_ = device_profile.id
            else:
                self.device_profile_id_ = False


class DeviceKeys(models.Model):
    _name = 'appserver.device_keys'
    _table = 'device_keys'
    _auto = False

    # TODO dev_eui must be primary key and defined as indicated below
    # dev_eui = fields.Many2one(required=True, comodel_name='appserver.device', ondelete='cascade')
    dev_eui = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    app_key = fields.Binary(required=True)
    join_nonce = fields.Integer(required=True)

class DeviceActivation(models.Model):
    _name = 'appserver.device_activation'
    _table = 'device_activation'
    _auto = False

    created_at = fields.Datetime(required=True)
    # TODO dev_eui must be primary key and defined as indicated below
    # dev_eui = fields.Many2one(required=True, comodel_name='appserver.device', ondelete='cascade')
    dev_eui = fields.Char()
    dev_addr = fields.Binary(required=True)
    app_s_key = fields.Binary(required=True)
    nwk_s_key = fields.Binary(required=True)

class DeviceQueue(models.Model):
    _name = 'appserver.device_queue'
    _table = 'device_queue'
    _auto = False

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    reference = fields.Char(size=100, required=True)
    # TODO dev_eui must be defined as indicated below
    # dev_eui = fields.Many2one(comodel_name='appserver.device', ondelete='cascade')
    dev_eui = fields.Char()
    confirmed = fields.Boolean(required=True, default=False)
    pending = fields.Boolean(required=True, default=False)
    fport = fields.Integer(required=True)
    data = fields.Binary(required=True)

class DeviceQueueMapping(models.Model):
    _name = 'appserver.device_queue_mapping'
    _table = 'device_queue_mapping'
    _auto = False

    created_at = fields.Datetime(required=True)
    reference = fields.Text(required=True)
    # TODO dev_eui must be defined as indicated below
    # dev_eui = fields.Many2one(comodel_name='appserver.device', ondelete='cascade')
    dev_eui = fields.Char()
    f_cnt = fields.Integer(required=True)

class GatewayProfile(models.Model):
    _name = 'appserver.gateway_profile'
    _table = 'gateway_profile'
    _auto = False

    # TODO gateway_profile_id must be primary key with uuid type
    gateway_profile_id = fields.Char()
    network_server_id = fields.Many2one(required=True, comodel_name='appserver.network_server')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    name = fields.Char(size=100, required=True)



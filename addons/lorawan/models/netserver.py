from odoo import models, fields, api


# TODO check all fields in models, because problems may arrive with numeric types
class Gateway(models.Model):
    _name = 'lorawan.gateway'
    _table = 'gateway'

    mac = fields.Binary()
    name = fields.Char(size=100, required=True)
    description = fields.Text()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    first_seen_at = fields.Datetime()
    last_seen_at = fields.Datetime()
    # TODO location field must be point type
    location = fields.Char(required=True, default='(0,0)')
    altitude = fields.Float(required=True, default=0)
    channel_configuration_id = fields.Many2one(required=True, comodel_name='lorawan.channel_configuration', ondelete='set null')
    # TODO gateway_profile_id must be defined as indicated below, in migrations file is not specified ondelete rule
    # gateway_profile_id = fields.Many2one(comodel_name='lorawan.gateway_profile')
    gateway_profile_id = fields.Char()
    ping = fields.Boolean(required=True, default=False)
    last_ping_id = fields.Many2one(comodel_name='lorawan.gateway_ping', ondelete='set null')
    last_ping_sent_at = fields.Datetime(required=True)
    network_server_id = fields.Many2one(comodel_name='lorawan.network_server', ondelete='set null')

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
    _table = 'gateway_stats'

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
    _table = 'frame_log'

    created_at = fields.Datetime(required=True)
    dev_eui = fields.Binary(required=True)
    # TODO rx_info_set and tx_info must have jsonb type
    rx_info_set = fields.Text()
    tx_info = fields.Text()
    phy_payload = fields.Binary(required=True)


class ChannelConfiguration(models.Model):
    _name = 'lorawan.channel_configuration'
    _table = 'channel_configuration'

    name = fields.Char(size=100, required=True)
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    band = fields.Char(size=20, required=True)
    channels = fields.Integer(required=True)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The name must be unique"),
    ]


class ExtraChannel(models.Model):
    _name = 'lorawan.extra_channel'
    _table = 'extra_channel'

    channel_configuration_id = fields.Many2one(required=True, comodel_name='lorawan.channel_configuration', ondelete='cascade')
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    modulation = fields.Char(size=10, required=True)
    frequency = fields.Integer(required=True)
    bandwidth = fields.Integer(required=True)
    bit_rate = fields.Integer(required=True)
    spread_factors = fields.Integer()


class DeviceProfile(models.Model):
    _name = 'lorawan.device_profile'
    _table = 'device_profile'

    # This fields coincide with fields from appserver-->start
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    # TODO device_profile_id must be primary key with uuid type
    device_profile_id = fields.Char()
    # This fields coincide with fields from appserver-->end

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

    # This fields are from appserver-->start
    network_server_id = fields.Many2one(required=True, comodel_name='lorawan.network_server')
    organization_id = fields.Many2one(required=True, comodel_name='lorawan.organization')
    name = fields.Char(size=100, required=True)
    # This fields are from appserver-->end

class ServiceProfile(models.Model):
    _name = 'lorawan.service_profile'
    _table = 'service_profile'

    # This fields coincide with fields from appserver-->start
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    # TODO device_profile_id must be primary key with uuid type
    service_profile_id = fields.Char()
    # This fields coincide with fields from appserver-->end

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
    channel_mask = fields.Binary()
    pr_allowed = fields.Boolean(required=True)
    hr_allowed = fields.Boolean(required=True)
    ra_allowed = fields.Boolean(required=True)
    nwk_geo_loc = fields.Boolean(required=True)
    target_per = fields.Integer(required=True)
    min_gw_diversity = fields.Integer(required=True)

    # This fields are from appserver-->start
    organization_id = fields.Many2one(required=True, comodel_name='lorawan.organization')
    network_server_id = fields.Many2one(required=True, comodel_name='lorawan.network_server')
    name = fields.Char(size=100, required=True)
    # This fields are from appserver-->end

class RoutingProfile(models.Model):
    _name = 'lorawan.routing_profile'
    _table = 'routing_profile'

    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    # TODO routing_profile_id must be primary key with uuid type
    routing_profile_id = fields.Char()
    as_id = fields.Char(size=255)
    ca_cert = fields.Text(required=True, default='')
    tls_cert = fields.Text(required=True, default='')
    tls_key = fields.Text(required=True, default='')

class Device(models.Model):
    _name = 'lorawan.device'
    _table = 'device'

    # This fields coincide with fields from appserver-->start
    # TODO dev_eui must be primary key
    dev_eui = fields.Binary()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    # TODO device_profile_id, service_profile_id, routing_profile_id must be defined as indicated below
    # device_profile_id = fields.Many2one(required=True, comodel_name='lorawan.device_profile', ondelete='cascade')
    # service_profile_id = fields.Many2one(required=True, comodel_name='lorawan.service_profile', ondelete='cascade')
    # routing_profile_id = fields.Many2one(required=True, comodel_name='lorawan.routing_profile', ondelete='cascade')
    device_profile_id = fields.Char()
    # This fields coincide with fields from appserver-->end

    service_profile_id = fields.Char()
    routing_profile_id = fields.Char()
    skip_fcnt_check = fields.Boolean(required=True, default=False)

    # This fields are from appserver-->start
    application_id = fields.Many2one(required=True, comodel_name='lorawan.application', ondelete='cascade')
    name = fields.Char(size=100, required=True)
    description = fields.Text(required=True)
    last_seen_at = fields.Datetime(required=True)
    device_status_battery = fields.Integer(required=True)
    device_status_margin = fields.Integer(required=True)
    # This fields are from appserver-->end

class DeviceActivation(models.Model):
    _name = 'lorawan.device_activation'
    _table = 'device_activation'

    # This fields coincide with fields from appserver-->start
    created_at = fields.Datetime(required=True)
    # TODO dev_eui must bedefined as indicated below
    # dev_eui = fields.Many2one(required=True, comodel_name='lorawan.device', ondelete='cascade')
    dev_eui = fields.Char()
    dev_addr = fields.Binary(required=True)
    nwk_s_key = fields.Binary(required=True)
    # This fields coincide with fields from appserver-->end

    join_eui = fields.Binary(required=True)
    dev_nonce = fields.Binary(required=True)

    # This fields are from appserver-->start
    app_s_key = fields.Binary(required=True)
    # This fields are from appserver-->end

class DeviceQueue(models.Model):
    _name = 'lorawan.device_queue'
    _table = 'device_queue'

    # This fields coincide with fields from appserver-->start
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    # TODO dev_eui must be defined as indicated below
    # dev_eui = fields.Many2one(comodel_name='lorawan.device', ondelete='cascade')
    dev_eui = fields.Char()
    confirmed = fields.Boolean(required=True)
    # This fields coincide with fields from appserver-->end

    frm_payload = fields.Binary()
    f_cnt = fields.Integer(required=True)
    f_port = fields.Integer(required=True)
    is_pending = fields.Boolean(required=True)
    # TODO emit_at_time_since_gps_epoch must be bigint
    emit_at_time_since_gps_epoch = fields.Integer()
    timeout_after = fields.Datetime(required=True)

    # This fields are from appserver-->start
    reference = fields.Char(size=100, required=True)
    pending = fields.Boolean(required=True, default=False)
    fport = fields.Integer(required=True)
    data = fields.Binary(required=True)
    # This fields are from appserver-->end


class GatewayProfile(models.Model):
    _name = 'lorawan.gateway_profile'
    _table = 'gateway_profile'

    # This fields coincide with fields from appserver-->start
    # TODO gateway_profile_id must be primary key with uuid type
    gateway_profile_id = fields.Char()
    created_at = fields.Datetime(required=True)
    updated_at = fields.Datetime(required=True)
    # This fields coincide with fields from appserver-->end
    # TODO channels must be with type smallint
    channels = fields.Integer(required=True)

    # This fields are from appserver-->start
    network_server_id = fields.Many2one(required=True, comodel_name='lorawan.network_server')
    name = fields.Char(size=100, required=True)
    # This fields are from appserver-->end

class GatewayProfileExtraChannel(models.Model):
    _name = 'gateway.gateway_profile_extra_channel'
    _table = 'gateway_profile_extra_channel'

    # TODO gateway_profile_id must be defined as indicated below
    # gateway_profile_id = fields.Many2one(required=True, comodel_name='lorawan.gateway_profile', ondelete='cascade')
    gateway_profile_id = fields.Char()
    modulation = fields.Char(size=10, required=True)
    frequency = fields.Integer(required=True)
    bandwidth = fields.Integer(required=True)
    bitrate = fields.Integer(required=True)
    # TODO spreading_factors must be with type smallint
    spreading_factors = fields.Integer()
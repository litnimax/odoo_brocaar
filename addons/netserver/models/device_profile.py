# -*- coding: utf-8 -*-
from odoo import models, fields, api


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
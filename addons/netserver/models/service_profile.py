# -*- coding: utf-8 -*-
from odoo import models, fields, api


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

# -*- coding: utf-8 -*-
from odoo import models, fields


class FrameLog(models.Model):
    _name = 'netserver.frame_log'
    _table = 'frame_log'
    _auto = False

    created_at = fields.Datetime(required=True)
    dev_eui = fields.Char(required=True)
    rx_info_set = fields.Text()
    tx_info = fields.Text()
    phy_payload = fields.Binary(required=True)

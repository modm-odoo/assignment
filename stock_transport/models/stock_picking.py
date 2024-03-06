#-*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import timedelta

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volumes = fields.Float(related="batch_id.total_volume", default=1, string="Volume")
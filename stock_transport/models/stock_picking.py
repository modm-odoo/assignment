#-*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import timedelta

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(default=1, string="Volume")
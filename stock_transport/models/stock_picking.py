#-*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import timedelta

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volumes = fields.Float(compute="_compute_volume", default=1, string="Volume")

    @api.depends()
    def _compute_volume(self):
        for record in self:
            volume = 0
            for move_line in record.move_line_ids:
                volume += move_line.product_id.volume * move_line.quantity

            record.volumes = volume
    
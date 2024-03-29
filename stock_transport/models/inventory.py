#-*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import *

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.dock")
    vehicle = fields.Many2one("fleet.vehicle")
    vehicle_category_id = fields.Many2one("fleet.vehicle.model.category")
    weight = fields.Float(compute="_compute_weight_volume", store=True)
    volume = fields.Float(compute="_compute_weight_volume", store=True)
    start_date = fields.Date(compute="_compute_dates", store=True)
    end_date = fields.Date(compute="_compute_dates", store=True)
    moves_count = fields.Integer(string="Move Lines", compute="_compute_moves_number", store=True)
    transfers_count = fields.Integer(string="Transfer Lines", compute="_compute_picking_number", store=True)
    total_weight = fields.Float(compute="_compute_weight_volume")
    total_volume = fields.Float(compute="_compute_weight_volume")

    @api.depends("vehicle_category_id","weight","volume")
    def _compute_weight_volume(self):
        for record in self:
            weight = 0
            volume = 0

            for move_line in record.move_line_ids:
                weight += move_line.product_id.weight * move_line.quantity
                volume += move_line.product_id.volume * move_line.quantity
                
            record.total_weight = weight
            record.total_volume = volume

            record.weight = (weight / record.vehicle_category_id.max_weight) * 100 if record.vehicle_category_id.max_weight != 0 else 0
            record.volume = (volume / record.vehicle_category_id.max_volume) * 100 if record.vehicle_category_id.max_volume != 0 else 0

    @api.depends("scheduled_date")
    def _compute_dates(self):
        for record in self:
            record.start_date = record.scheduled_date
            record.end_date = record.scheduled_date + timedelta(days=2)

    @api.depends("move_line_ids")
    def _compute_moves_number(self):
        for record in self:
            record.moves_count = len(record.move_line_ids)

    @api.depends("picking_ids")
    def _compute_picking_number(self):
        for record in self:
            record.transfers_count = len(record.picking_ids)

    @api.depends("vehicle_category_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.name} : ({rec.weight},{rec.volume})'

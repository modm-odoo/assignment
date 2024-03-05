#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, Command, fields, api

class InheritedModel2(models.Model):
    _inherit = ["stock.picking.batch"]

    dock_id = fields.Many2one("stock.transport.dock")
    vehicle = fields.Many2one("fleet.vehicle")
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category')
    weight = fields.Float(compute="_compute_weight_volume")
    volume = fields.Float(compute="_compute_weight_volume")
    leave_id = fields.Many2one(
        'resource.calendar.leaves',
        help='Slot into workcenter calendar once planned',
        check_company=True, copy=False)
    date_start = fields.Datetime(
        'Start',
        compute='_compute_dates',
        inverse='_set_dates',
        store=True, copy=False)
    date_finished = fields.Datetime(
        'End',
        compute='_compute_dates',
        inverse='_set_dates',
        store=True, copy=False)
    state = fields.Selection([
        ('pending', 'Waiting for another Vehicle'),
        ('waiting', 'Waiting for vehicle'),
        ('ready', 'Ready'),
        ('progress', 'In Progress'),
        ('done', 'Finished'),
        ('cancel', 'Cancelled')], string='Status',
        compute='_compute_state', store=True,
        default='pending', copy=False, readonly=True, recursive=True, index=True)

    @api.depends("vehicle_category_id")
    def _compute_weight_volume(self):
        move_line_ids=[]

        weight = 0
        volume = 0

        for move_line_id in self.move_line_ids:
            move_line_ids.append(move_line_id.id)

        move_lines = self.env["stock.move.line"].browse(move_line_ids)
        # breakpoint()
        for move_line in move_lines:
            weight += move_line.product_id.weight * move_line.quantity
            volume += move_line.product_id.volume * move_line.quantity

        if self.vehicle_category_id.max_weight != 0:
            self.weight = weight / self.vehicle_category_id.max_weight
        else:
            self.weight = 0

        if self.vehicle_category_id.max_volume != 0:
            self.volume = volume / self.vehicle_category_id.max_volume
        else:
            self.volume = 0

    @api.depends('leave_id')
    def _compute_dates(self):
        for vehicle in self:
            vehicle.date_start = vehicle.leave_id.date_from
            vehicle.date_finished = vehicle.leave_id.date_to

    def _set_dates(self):
        for wo in self.sudo():
            if wo.leave_id:
                if (not wo.date_start or not wo.date_finished):
                    raise UserError(_("It is not possible to unplan one single Work Order. "
                              "You should unplan the Manufacturing Order instead in order to unplan all the linked operations."))
                wo.leave_id.write({
                    'date_from': wo.date_start,
                    'date_to': wo.date_finished,
                })
            elif wo.date_start and wo.date_finished:
                wo.leave_id = wo.env['resource.calendar.leaves'].create({
                    'name': wo.display_name,
                    'date_from': wo.date_start,
                    'date_to': wo.date_finished,
                    'resource_id': wo.vehicle.id,
                    'time_type': 'other',
                })
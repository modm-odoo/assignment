#-*- coding: utf-8 -*-

from odoo import models, Command, fields, api

class InheritedModel(models.Model):
    _inherit = ["fleet.vehicle.model.category"]

    max_weight = fields.Float(string="Max Weight(kg)", default=1)
    max_volume = fields.Float(string="Max Volume(m\u00b3)", default=1)

    @api.depends('name', 'max_weight', 'max_volume')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.name}/({rec.max_weight},{rec.max_volume})'
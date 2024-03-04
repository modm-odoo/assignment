#-- coding: utf-8 --

from odoo import fields, models

class StockTransportDock(models.Model):
    _name = "stock.transport.dock"

    name = fields.Char("Dock Name", required=True)

    _sql_constraints = [
        ("unique_dock_name", "unique(name)", "Dock exists"),
    ]
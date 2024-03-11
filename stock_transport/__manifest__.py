#-*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Stock Transport",
    "version": "1.0",
    "summary": "It is a stock transport application",
    "installable": True,
    "application": True,
    "license": "OEEL-1",
    "depends": ["base", "stock_picking_batch", "fleet", "mail"], 
    "data": [
        "security/ir.model.access.csv",
        "views/fleet.xml",
        "views/inventory.xml",
    ]
}
#-*- coding: utf-8 -*-
#Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Stock Trans",
    "version": "1.0",
    "summary": "It is a stock transport application",
    "installable": True,
    "application": True,
    "auto_install": True,
    "license": "OEEL-1",
    "depends": ["base", "stock", "fleet",], 
    "data": [
        "views/inherited_setting.xml",
    ]
}
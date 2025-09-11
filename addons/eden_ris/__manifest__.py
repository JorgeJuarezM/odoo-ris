# -*- coding: utf-8 -*-
{
    "name": "eden_ris",
    "summary": "RIS for Odoo",
    "description": "RIS for Odoo",
    "author": "Jorge Juarez",
    "website": "https://www.jorgejuarez.net",
    "category": "Healthcare",
    "version": "0.1",
    "depends": ["base", "sale", "sale_management", "partner_firstname"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
}

# -*- coding: utf-8 -*-
from odoo import fields, models


class RisProduct(models.Model):
    _name = "ris.product"
    _inherits = {"product.product": "product_id"}
    _description = "Ris Product"

    product_id = fields.Many2one("product.product", "Product", required=True)

    description = fields.Text("Description")
    product_type_id = fields.Many2one("ris.product.type", "Product Type", required=True)
    active = fields.Boolean("Active", default=True)

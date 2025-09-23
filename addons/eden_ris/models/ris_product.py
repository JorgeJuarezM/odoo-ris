# -*- coding: utf-8 -*-
from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class RisProduct(models.Model):
    _name = "ris.product"
    _inherits = {"product.product": "product_id"}
    _description = "Ris Product"

    product_id = fields.Many2one("product.product", "Product", required=True)

    description = fields.Text("Description")
    product_type_id = fields.Many2one("ris.product.type", "Product Type", required=True)
    active = fields.Boolean("Active", default=True)


    def create(self, vals):
        products = super(RisProduct, self).create(vals)
        for product in products:
            product.with_delay()._send_to_ris()
        return products
    
    def _send_to_ris(self):
        for product in self:
            _logger.info("Send to RIS: %s", product.name)
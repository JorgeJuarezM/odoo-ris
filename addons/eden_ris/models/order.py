from odoo import fields, models


class RisOrder(models.Model):
    _name = "ris.order"
    _inherits = {"sale.order": "sale_id"}

    sale_id = fields.Many2one(
        "sale.order", string="Sale Order", required=True, ondelete="cascade"
    )

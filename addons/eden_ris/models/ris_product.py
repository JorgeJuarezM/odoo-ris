# -*- coding: utf-8 -*-
from odoo import fields, models


class RisProduct(models.Model):
    _name = "ris.product"
    _description = "Ris Product"

    name = fields.Char("Name", required=True)
    code = fields.Char("Code", required=True)
    modality_id = fields.Many2one("ris.modality", "Modality", required=True)

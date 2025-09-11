from odoo import fields, models


class ApiSettings(models.Model):
    _name = "api.settings"
    _description = "Api Settings"

    name = fields.Char()
    url = fields.Char()
    token = fields.Char()

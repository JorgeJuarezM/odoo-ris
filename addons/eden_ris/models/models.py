# -*- coding: utf-8 -*-

import logging

import requests
from odoo import fields, models

_log = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def send_to_ris(self):
        for order in self:
            assert isinstance(order, SaleOrder)
            order._send_to_ris()

    def _send_to_ris(self):
        for line in self.order_line:
            self._send_line_to_ris(self, line)

    def _send_line_to_ris(self, order: "SaleOrder", order_line):
        data = {
            "folio": self._compute_ris_folio(order, order_line),
            "description": order_line.name,
            "patient_name": order.partner_id.name,
            "patient_gender": order.partner_id.gender,
            "patient_birthdate": order.partner_id.birth_date.strftime("%Y-%m-%d"),
            "modality": "CR",
            "study_name": order_line.product_id.name,
            "study_code": order_line.product_id.default_code,
            "facility_identifier": "eva-centro",
        }

        _log.info(data)

        req = requests.post(
            "https://middleware-staging.dev-land.space/api/v1/orders/",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Token 4ac1d9f3c597209cb6460023a62c3ba9bb198eef",
            },
        )
        _log.info(req.json())
        req.raise_for_status()

    def _compute_ris_folio(self, order: "SaleOrder", order_line):
        base_folio = order.name
        sequence = str(order_line.id).rjust(6, "0")
        return f"{base_folio}-{sequence}"


class ResPartner(models.Model):
    _inherit = "res.partner"

    gender = fields.Selection(
        selection=[
            ("O", "Other"),
            ("M", "Male"),
            ("F", "Female"),
        ],
        string="Gender",
    )

    birth_date = fields.Date(string="Birth Date")

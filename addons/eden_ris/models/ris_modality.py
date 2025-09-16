# -*- coding: utf-8 -*-
from odoo import fields, models


class RisModality(models.Model):
    _name = "ris.modality"
    _description = "Ris Modality"

    name = fields.Char("Name", required=True, translate=True)
    dicom_modality = fields.Selection(
        [
            ("CT", "CT"),
            ("MR", "MR"),
            ("US", "US"),
            ("XA", "XA"),
            ("DX", "DX"),
            ("CR", "CR"),
            ("MG", "MG"),
        ],
        "DICOM Modality",
    )
    active = fields.Boolean("Active", default=True)

    def _compute_display_name(self):
        for modality in self:
            modality.display_name = f"{modality.dicom_modality} - {modality.name}"

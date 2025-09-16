from odoo import fields, models


class RisPatient(models.Model):
    _name = "ris.patient"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one("res.partner", "Patient", required=True)

    gender = fields.Selection(
        [("M", "Male"), ("F", "Female"), ("O", "Other")], string="Gender"
    )
    birth_date = fields.Date(string="Birth Date")

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.ref}] {record.name}"

    def create(self, vals):
        if "ref" not in vals:
            vals["ref"] = self.env["ir.sequence"].next_by_code("patient.mrn.sequence")
        return super(RisPatient, self).create(vals)

from odoo import fields, models


class RisProductType(models.Model):
    """
    Ris Product Type
    """

    _name = "ris.product.type"
    _description = "Product Type"

    name = fields.Char("Name", required=True)
    code = fields.Char("Code", required=True, unique=True)
    modality_id = fields.Many2one("ris.modality", "Modality")

    active = fields.Boolean("Active", default=True)

    def _name_search(
        self,
        name="",
        domain=None,
        operator="ilike",
        limit=None,
        order=None,
    ):
        """
        Override name_search to allow searching by code
        """
        domain = ["|", ("name", operator, name), ("code", operator, name)]
        return self._search(domain, limit=limit, order=order)

    def _compute_display_name(self):
        """
        Compute display name
        """
        for record in self:
            record.display_name = "[%s] %s" % (record.code, record.name)

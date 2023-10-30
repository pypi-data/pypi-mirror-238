# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FieldServiceTypeRole(models.Model):
    _name = "field_service_type.role"
    _description = "Field Service Type - Role"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="field_service_type",
        required=True,
        ondelete="cascade",
    )
    role_id = fields.Many2one(
        string="Role",
        comodel_name="field_service_role",
        required=True,
        ondelete="restrict",
    )

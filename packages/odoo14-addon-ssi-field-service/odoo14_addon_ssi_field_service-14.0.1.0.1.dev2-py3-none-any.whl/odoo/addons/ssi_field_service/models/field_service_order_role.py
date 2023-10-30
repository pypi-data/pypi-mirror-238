# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FieldServiceOrderRole(models.Model):
    _name = "field_service_order.role"
    _description = "Field Service Order - Role"

    order_id = fields.Many2one(
        string="# Order",
        comodel_name="field_service_order",
        required=True,
        ondelete="cascade",
    )
    role_id = fields.Many2one(
        string="Role",
        comodel_name="field_service_role",
        required=True,
        ondelete="restrict",
    )
    asignee_id = fields.Many2one(
        string="Asignee",
        comodel_name="res.partner",
        ondelete="restrict",
        domain=[
            ("is_company", "=", False),
        ],
    )

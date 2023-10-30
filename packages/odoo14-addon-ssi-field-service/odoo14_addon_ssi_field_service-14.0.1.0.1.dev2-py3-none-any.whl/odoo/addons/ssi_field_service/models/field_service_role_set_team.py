# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FieldServiceRoleSetTeam(models.Model):
    _name = "field_service_role_set.team"
    _description = "Field Service Role Set - Team"
    _order = "set_id, sequence"

    set_id = fields.Many2one(
        string="Role Set",
        comodel_name="field_service_role_set",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=1,
        required=True,
    )
    role_id = fields.Many2one(
        string="Role",
        comodel_name="field_service_role",
        required=True,
        ondelete="restrict",
    )
    quantity = fields.Integer(
        string="Quantity",
        required=True,
        default=1,
    )

    def _create_role(self, fso):
        self.ensure_one()

        Role = self.env["field_service_order.role"]

        for _counter in range(0, self.quantity):
            Role.create(self._prepare_create_role(fso))

    def _prepare_create_role(self, fso):
        self.ensure_one()
        return {
            "order_id": fso.id,
            "role_id": self.role_id.id,
        }

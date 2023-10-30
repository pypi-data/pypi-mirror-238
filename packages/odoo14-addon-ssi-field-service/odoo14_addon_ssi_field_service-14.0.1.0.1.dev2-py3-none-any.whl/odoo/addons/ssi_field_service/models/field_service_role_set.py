# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FieldServiceRoleSet(models.Model):
    _name = "field_service_role_set"
    _inherit = ["mixin.master_data"]
    _description = "Field Service Role Set"

    team_ids = fields.One2many(
        string="Teams",
        comodel_name="field_service_role_set.team",
        inverse_name="set_id",
    )

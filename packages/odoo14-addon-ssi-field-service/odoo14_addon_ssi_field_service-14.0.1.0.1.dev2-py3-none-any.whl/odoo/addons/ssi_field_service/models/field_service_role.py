# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class FieldServiceRole(models.Model):
    _name = "field_service_role"
    _inherit = ["mixin.master_data"]
    _description = "Field Service Role"

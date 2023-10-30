# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class FieldServiceTimeSlot(models.Model):
    _name = "field_service_time_slot"
    _inherit = ["mixin.master_data"]
    _description = "Field Service Time Slot"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    time_start = fields.Float(
        string="Start",
        required=True,
    )
    time_end = fields.Float(
        string="End",
        required=True,
    )

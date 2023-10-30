# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class GroupFieldServiceOrderRecurringPattern(models.Model):
    _name = "group_field_service_order.recurring_pattern"
    _description = "Group Field Service Order - Recurring Pattern"

    order_id = fields.Many2one(
        string="# Order",
        comodel_name="group_field_service_order",
        required=True,
        ondelete="cascade",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    location_id = fields.Many2one(
        string="Location",
        comodel_name="res.partner",
        required=True,
    )
    frequency_id = fields.Many2one(
        string="Frequency",
        comodel_name="frequency",
        required=True,
        ondelete="restrict",
    )
    time_slot_id = fields.Many2one(
        string="Time Slot",
        comodel_name="field_service_time_slot",
        required=True,
        ondelete="restrict",
    )
    role_set_id = fields.Many2one(
        string="Role Set",
        comodel_name="field_service_role_set",
        required=True,
        ondelete="restrict",
    )

    def action_create_field_service_order(self):
        for record in self.sudo():
            record._create_field_service_order()

    def _create_field_service_order(self):
        self.ensure_one()
        for date_order in self.frequency_id._get_rrule(
            fields.Datetime.to_datetime(self.date_start),
            fields.Datetime.to_datetime(self.date_end),
        ):
            date_order = fields.Date.to_date(date_order)
            self.env["field_service_order"].create(
                self._prepare_create_field_service_order(date_order)
            )

    def _prepare_create_field_service_order(self, date_order):
        self.ensure_one()
        return {
            "group_order_id": self.order_id.id,
            "partner_id": self.order_id.partner_id.id,
            "contact_partner_id": self.order_id.contact_partner_id.id,
            "location_id": self.location_id.id,
            "type_id": self.order_id.type_id.id,
            "date": date_order,
            "time_slot_id": self.time_slot_id.id,
            "role_set_id": self.role_set_id.id,
        }

# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class FieldServiceOrder(models.Model):
    _name = "field_service_order"
    _inherit = [
        "mixin.transaction_terminate",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_ready",
        "mixin.transaction_partner",
    ]
    _description = "Field Service Order"

    # Multiple Approval Attribute
    _approval_from_state = "open"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,ready,open,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "open_ok",
        "done_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_ready",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_open",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_ready",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "ready"

    allowed_location_ids = fields.Many2many(
        string="Allowed Locations",
        comodel_name="res.partner",
        compute="_compute_allowed_location_ids",
        store=False,
    )
    location_id = fields.Many2one(
        string="Location",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    group_order_id = fields.Many2one(
        string="# Group Order",
        comodel_name="group_field_service_order",
        readonly=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="field_service_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    time_slot_id = fields.Many2one(
        string="Time Slot",
        comodel_name="field_service_time_slot",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    role_set_id = fields.Many2one(
        string="Role Set",
        comodel_name="field_service_role_set",
        readonly=True,
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    role_ids = fields.One2many(
        string="Roles",
        comodel_name="field_service_order.role",
        inverse_name="order_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_location_ids(self):
        Partner = self.env["res.partner"]
        for record in self:
            result = []
            if record.partner_id:
                criteria = [
                    ("commercial_partner_id", "=", record.partner_id.id),
                    ("id", "!=", record.partner_id.id),
                    ("type", "!=", "contact"),
                ]
                result = Partner.search(criteria).ids
            record.allowed_location_ids = result

    @api.onchange(
        "partner_id",
    )
    def onchange_location_id(self):
        self.location_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    def action_create_role(self):
        for record in self.sudo():
            record._create_role()

    def _create_role(self):
        self.ensure_one()
        if not self.role_set_id:
            return True

        self.role_ids.unlink()

        for team in self.role_set_id.team_ids:
            team._create_role(self)

    @api.model
    def _get_policy_field(self):
        res = super(FieldServiceOrder, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "ready_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

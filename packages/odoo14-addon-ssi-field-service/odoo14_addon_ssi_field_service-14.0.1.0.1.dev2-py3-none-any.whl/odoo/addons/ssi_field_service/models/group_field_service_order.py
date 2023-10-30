# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class GroupFieldServiceOrder(models.Model):
    _name = "group_field_service_order"
    _inherit = [
        "mixin.transaction_terminate",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_partner",
        "mixin.transaction_date_duration",
    ]
    _description = "Group Field Service Order"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,open,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

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
    recurring_pattern_ids = fields.One2many(
        string="Recurring Pattern",
        comodel_name="group_field_service_order.recurring_pattern",
        inverse_name="order_id",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_location_ids = fields.Many2many(
        string="Allowed Locations",
        comodel_name="res.partner",
        compute="_compute_allowed_location_ids",
        store=False,
    )
    order_ids = fields.One2many(
        string="Field Service Order",
        comodel_name="field_service_order",
        inverse_name="group_order_id",
        readonly=True,
    )
    order_status = fields.Selection(
        string="Order Status",
        selection=[
            ("no_order", "No Order"),
            ("open", "Open"),
            ("done", "Done"),
        ],
        compute="_compute_order_status",
        store=True,
    )

    @api.depends(
        "order_ids",
        "order_ids.state",
    )
    def _compute_order_status(self):
        for record in self:
            result = "no_order"
            criteria = [
                ("group_order_id", "=", record.id),
            ]
            orders = self.env["field_service_order"].search(criteria)
            if len(orders) > 0:
                result = "done"
            for order in orders:
                if order.state not in ["done", "cancel", "terminate"]:
                    result = "open"
                    break
            record.order_status = result

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
        "type_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    def action_create_fso(self):
        for record in self.sudo():
            record._10_delete_fso()
            record._20_create_fso()

    @ssi_decorator.post_open_action()
    def _20_create_fso(self):
        self.ensure_one()
        for recurring_pattern in self.recurring_pattern_ids:
            recurring_pattern._create_field_service_order()
        self.order_ids.action_create_role()

    @ssi_decorator.post_open_action()
    @ssi_decorator.post_cancel_action()
    def _10_delete_fso(self):
        self.ensure_one()
        self.order_ids.unlink()

    @api.model
    def _get_policy_field(self):
        res = super(GroupFieldServiceOrder, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
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

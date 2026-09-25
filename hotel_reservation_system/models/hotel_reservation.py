from odoo import api, fields, models, _,Command
from odoo.exceptions import ValidationError,UserError

from email.policy import default


class HotelReservation(models.Model):
    _name = "hotel.reservation"
    _description = "Hotel Reservation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "reservation_no"
    _order = "check_in_date desc"



    reservation_no = fields.Char(
        string="Reservation No",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        tracking=True,
    )
    invoice_id = fields.Many2one('account.move', string="Invoice")
    invoice_count = fields.Integer(
        compute="_compute_invoice_count",
    )

    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = 1 if rec.invoice_id else 0

    def action_view_invoice(self):
        self.ensure_one()

        if not self.invoice_id:
            return False

        return {
            "type": "ir.actions.act_window",
            "name": "Invoice",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": self.invoice_id.id,
            "target": "current",
        }
    active = fields.Boolean(default=True)

    branch_id = fields.Many2one(
        "res.company",
        string="Branch",
        required=True,
        default=lambda self: self.env.company,
    )

    guest_id = fields.Many2one(
        "res.partner",
        string="Guest",
        required=True,
        tracking=True,
    )

    room_id = fields.Many2one(
        "hotel.room",
        string="Room",
        required=True,
        tracking=True,
        domain="[('status','=','available')]",
    )

    room_type_id = fields.Many2one(
        "hotel.room.type",
        string="Room Type",
        related="room_id.room_type_id",
        store=True,
        readonly=True,
    )

    check_in_date = fields.Datetime(
        string="Check In",
        required=True,
        tracking=True,
    )

    check_out_date = fields.Datetime(
        string="Check Out",
        required=True,
        tracking=True,
    )

    no_of_nights = fields.Integer(
        string="Nights",
        compute="_compute_nights",
        store=True,
    )

    adults = fields.Integer(
        default=1,
    )

    children = fields.Integer(
        default=0,
    )

    status = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
        ("cancelled", "Cancelled"),
    ], default="draft", tracking=True)

    payment_status = fields.Selection([
        ("unpaid", "Unpaid"),
        ("partial", "Partially Paid"),
        ("paid", "Paid"),
    ], default="unpaid", tracking=True)

    room_price = fields.Float(
        string="Room Rate",
        compute="_compute_room_price",
        store=True,
    )

    total_amount = fields.Float(
        string="Total Amount",
        compute="_compute_total_amount",
        store=True,
    )

    notes = fields.Text()

    pos_order_ids = fields.One2many(
        "pos.order", "reservation_id", string="POS Orders"
    )
    pos_order_count = fields.Integer(
        string="POS Order Count", compute="_compute_pos_order_count"
    )

    def _compute_pos_order_count(self):
        for reservation in self:
            reservation.pos_order_count = len(reservation.pos_order_ids)

    extra_charges_line_ids = fields.One2many(
        "extra.services.line", "extra_reservation_id", string="Extra Services"
    )
    amount_total = fields.Float(
        string="Total Amount", compute="_compute_amount_total", store=True
    )

    multiple_rooms = fields.Boolean("Multi Room", default=False)
    room_line_ids = fields.One2many(
        "hotel.reservation.room.line", "reservation_id", string="Rooms"
    )
    @api.depends("extra_charges_line_ids.price_subtotal")
    def _compute_amount_total(self):
        for reservation in self:
            reservation.amount_total = sum(
                reservation.extra_charges_line_ids.mapped("price_subtotal")
            )


    @api.depends("check_in_date", "check_out_date")
    def _compute_nights(self):
        for rec in self:
            rec.no_of_nights = 0
            if rec.check_in_date and rec.check_out_date:
                delta = rec.check_out_date.date() - rec.check_in_date.date()
                rec.no_of_nights = max(delta.days, 1)

    @api.depends("room_id", "room_id.price_override", "room_id.room_type_id.base_price")
    def _compute_room_price(self):
        for rec in self:
            if rec.room_id:
                rec.room_price = (
                    rec.room_id.price_override
                    or rec.room_id.room_type_id.base_price
                )
            else:
                rec.room_price = 0.0

    @api.depends("room_price", "no_of_nights")
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.room_price * rec.no_of_nights

    @api.constrains("check_in_date", "check_out_date")
    def _check_dates(self):
        for rec in self:
            if rec.check_in_date >= rec.check_out_date:
                raise ValidationError(
                    _("Check-out date must be after check-in date.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("reservation_no", _("New")) == _("New"):
                vals["reservation_no"] = sequence.next_by_code(
                    "hotel.reservation"
                ) or _("New")
        return super().create(vals_list)

    # ---------------- Buttons ---------------- #

    def action_confirm(self):
        for rec in self:
            rec.status = "confirmed"
            rec.room_id.status = "reserved"

    def action_check_in(self):
        for rec in self:
            rec.status = "checked_in"
            rec.room_id.status = "occupied"

    def action_check_out(self):
        for rec in self:
            rec.status = "checked_out"
            rec.room_id.status = "available"

    def action_cancel(self):
        for rec in self:
            rec.status = "cancelled"
            rec.room_id.status = "available"

    def action_create_invoice(self):
        AccountMove = self.env["account.move"]


        product = self.env["product.product"].search([
            ("name", "=", "Room Charges")
        ], limit=1)

        if not product:
            raise UserError(
                "Please create a product named 'Room Charges'."
            )

        for rec in self:

            if rec.invoice_id:
                raise UserError("Invoice already created.")

            invoice = AccountMove.create({
                "move_type": "out_invoice",
                "partner_id": rec.guest_id.id,
                "invoice_origin": rec.reservation_no,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create({
                        "product_id": product.id,
                        "name": f"{rec.room_id.name} ({rec.check_in_date} - {rec.check_out_date})",
                        "quantity": rec.no_of_nights,
                        "price_unit": rec.room_price,
                    })
                ],
            })

            rec.invoice_id = invoice.id






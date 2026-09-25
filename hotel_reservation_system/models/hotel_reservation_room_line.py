from odoo import api, fields, models

class HotelReservationRoomLine(models.Model):
    _name = "hotel.reservation.room.line"
    _description = "Hotel Reservation Room Line"

    reservation_id = fields.Many2one(
        "hotel.reservation", string="Reservation",
        required=True, ondelete="cascade"
    )
    room_id = fields.Many2one("hotel.room", string="Room", required=True)
    room_type_id = fields.Many2one(
        related="room_id.room_type_id", string="Room Type", store=True, readonly=True
    )
    price_unit = fields.Float(string="Price per Night", default=0.0)

    # price_subtotal = fields.Float(
    #     string="Subtotal", compute="_compute_price_subtotal", store=True
    # )

    extra_service_line_ids = fields.One2many(
        "extra.services.line", "room_line_id", string="Extra Services"
    )
    extra_services_total = fields.Float(
        string="Services Total", compute="_compute_extra_services_total", store=True
    )

    # @api.depends("price_unit", "nights")
    # def _compute_price_subtotal(self):
    #     for line in self:
    #         line.price_subtotal = line.price_unit * (line.nights or 1)

    # @api.depends("extra_service_line_ids.price_subtotal")
    # def _compute_extra_services_total(self):
    #     for line in self:
    #         line.extra_services_total = sum(
    #             line.extra_service_line_ids.mapped("price_subtotal")
    #         )

    @api.onchange("room_id")
    def _onchange_room_id(self):
        if self.room_id and hasattr(self.room_id, "list_price"):
            self.price_unit = self.room_id.list_price
from odoo import fields, models

class PosOrder(models.Model):
    _inherit = "pos.order"

    room_id = fields.Many2one(
        "hotel.room",
        string="Room",
    )

    reservation_id = fields.Many2one("hotel.reservation", string="Reservation")

    def _order_fields(self, ui_order):
        vals = super()._order_fields(ui_order)
        vals["room_id"] = ui_order.get("room_id")
        vals["reservation_id"] = ui_order.get("reservation_id")
        return vals

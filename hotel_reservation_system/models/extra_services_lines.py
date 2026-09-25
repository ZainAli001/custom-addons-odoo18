from odoo import api, fields, models

class ExtraServicesLine(models.Model):
    _name = "extra.services.line"
    _description = "Extra Services Line"

    room_line_id = fields.Many2one(
        "hotel.reservation.room.line", string="Room Line",
        required=True, ondelete="cascade"
    )
    extra_reservation_id = fields.Many2one(
        "hotel.reservation", string="Reservation",
        required=True, ondelete="cascade"
    )
    product_id = fields.Many2one(
        "product.product", string="Product", required=True
    )
    price_unit = fields.Float(
        string="Unit Price",
        default=1.0,
    )
    quantity = fields.Float(string="Quantity", default=1.0)
    price_subtotal = fields.Float(
        string="Subtotal", compute="_compute_price_subtotal", store=True
    )

    @api.depends("price_unit", "quantity")
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.quantity

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
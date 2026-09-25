from odoo import models, fields

class HotelFloor(models.Model):
    _name = "hotel.floor"
    _description = "Hotel Floor"
    _order = "sequence"

    sequence = fields.Integer(default=10)
    name = fields.Char(
        required=True,
    )
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)

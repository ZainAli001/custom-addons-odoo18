from odoo import models,api ,fields

class HotelAmenity(models.Model):
    _name = "hotel.amenity"
    _description = "Room Amenity"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, tracking=True)
    code = fields.Char()
    description = fields.Text()
    image = fields.Image()

    active = fields.Boolean(default=True)
from odoo import api, fields, models

class HotelRoomType(models.Model):
    _name = "hotel.room.type"
    _description = "Hotel Room Type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    name = fields.Char(
        string="Room Type",
        required=True,
        tracking=True,
    )

    code = fields.Char(
        string="Code",
        required=True,
        tracking=True,
    )

    description = fields.Text()

    image = fields.Image(string="Image")

    capacity = fields.Integer(
        string="Maximum Capacity",
        default=2,
    )

    adult_capacity = fields.Integer(
        string="Adults",
        default=2,
    )

    child_capacity = fields.Integer(
        string="Children",
        default=0,
    )

    bed_type = fields.Selection([
        ("single", "Single"),
        ("double", "Double"),
        ("queen", "Queen"),
        ("king", "King"),
        ("twin", "Twin"),
    ], default="double")

    no_of_beds = fields.Integer(
        string="Number of Beds",
        default=1,
    )

    room_size = fields.Float(
        string="Room Size (sq ft)",
    )

    base_price = fields.Float(
        string="Base Price",
        required=True,
    )

    weekend_price = fields.Float(
        string="Weekend Price",
    )

    extra_bed_price = fields.Float(
        string="Extra Bed Price",
    )

    refundable = fields.Boolean(
        default=True,
    )

    breakfast_included = fields.Boolean()

    lunch_included = fields.Boolean()

    dinner_included = fields.Boolean()

    check_in_time = fields.Float(
        default=14.0,
        string="Check In Time",
    )

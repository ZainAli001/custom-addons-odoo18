from odoo import models, fields,api


class HotelRoom(models.Model):
    _name = 'hotel.room'

    name = fields.Char(string="Room Number", required=True)
    branch_id = fields.Many2one(
        "res.company",
        string="Branch",
        required=True,
    )

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        return {
            'domain': {
                'branch_id': [('id', 'in', self.env.company.child_ids.ids)]
            }
        }
    room_type_id = fields.Many2one(
        "hotel.room.type",
        string="Room Type",
        required=True,
    )
    floor_id = fields.Many2one(
        "hotel.floor",
        string="Floor",
    )

    status = fields.Selection([
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("occupied", "Occupied"),
        ("cleaning", "Cleaning"),
        ("maintenance", "Maintenance"),
        ("blocked", "Blocked"),
    ], default="available")

    housekeeping_status = fields.Selection([
        ("clean", "Clean"),
        ("dirty", "Dirty"),
        ("inspected", "Inspected"),
    ], default="clean")

    price_override = fields.Float(
        string="Custom Price"
    )

    description = fields.Text()

    active = fields.Boolean(default=True)
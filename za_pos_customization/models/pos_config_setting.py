from odoo import fields, models

class PosConfig(models.Model):
    _inherit = "pos.config"

    module_room_management = fields.Boolean(
        string="Room Management",
        help="Enable room selection on orders",
    )

    def _load_pos_data(self, data):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(self.id)
        data = self.search_read(domain, fields, load=False)
        print("fields",fields)
        if not data[0]['use_pricelist']:
            data[0]['pricelist_id'] = False

        return {
            'data': data,
            'fields': fields,
        }

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_module_room_management = fields.Boolean(
        related="pos_config_id.module_room_management",
        readonly=False,
        string="Room Management",
    )
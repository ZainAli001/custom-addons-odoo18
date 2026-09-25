/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    setup(vals, options) {
        super.setup(...arguments);
        vals = vals || {};
        this.room_id = vals.room_id || false;
    },
    set_room(room_id,reservation_id) {
        this.room_id = room_id;
        this.reservation_id = reservation_id;
    },
    get_room() {
        return this.room_id;
    },
    serialize(options) {
        const json = super.serialize(...arguments);
        json.room_id = this.room_id;
        json.reservation_id = this.reservation_id;

        return json;
    },
});
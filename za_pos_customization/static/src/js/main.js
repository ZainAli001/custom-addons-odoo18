/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { RoomPopup } from "@za_pos_customization/js/room_popup";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(ControlButtons.prototype, {
    async onClickRoom() {
        const room = await makeAwaitable(
            this.dialog,
            RoomPopup,
            {}
        );
        if (room) {
            const order = this.pos.get_order();
            order.set_room(room.room_id[0],room.id);
            room.id;
            console.log("order",order);
        }
    },
});

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        if (this.pos.config.module_room_management && !order.get_room()) {
            this.notification.add("Please select a room before validating the order.", {
                type: "danger",
            });
            return;
        }
        return super.validateOrder(...arguments);
    },
});
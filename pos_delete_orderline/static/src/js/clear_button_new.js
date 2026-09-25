/** @odoo-module **/
console.log("Enterrrrr");
import { Component } from "@odoo/owl";
import { useListener } from "@web/core/utils/hooks";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class OrderLineClearAll extends Component {
    static template = "pos_delete_orderline.OrderLineClearAll";
    setup() {
        this.pos = usePos();
        useListener("click", this.onClick);
    }

    async onClick() {
        const order = this.pos.get_order();
        console.log('order',order);
        if (!order) return;
        const lines = order.get_orderlines();
        for (let line of lines) {
            order.remove_orderline(line);
        }
    }
}
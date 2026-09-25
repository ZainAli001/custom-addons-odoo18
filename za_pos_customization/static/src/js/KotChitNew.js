/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { renderToString } from "@web/core/utils/render";

export class KotChitButton extends Component {
    static template = "ah_pos_kot_chit.KotChitButton";

    setup() {
        this.pos = usePos();
        this.orm = useService("orm");
    }

    async onClick() {
        const order = this.pos.get_order();
        if (!order) {
            return;
        }

        const customer = order.get_partner();

        const orderlines = order.get_orderlines().map(line => ({
            product_name: line.get_product().display_name,
            qty: line.get_quantity(),
            price: line.get_unit_price(),
            discount: line.get_discount(),
            note: line.get_note(),
        }));

        let member_code = "";
        let member_name = "";
        let guest_name = "";

        if (customer) {
            if (customer.parent_partner_id) {
                guest_name = customer.name;
                member_name = customer.parent_partner_id[1];
                member_code = customer.membership_no;
            } else {
                member_name = customer.name;
                member_code = customer.membership_no;
            }
        }

        const now = new Date();
        console.log("testt1");
        const receiptData = {
            company_name: this.pos.company.name,
            company_image: this.pos.company_logo_base64,
            order_name: order.name,
            table: order.table ? order.table.name : "",
            waiter_name: order.waiter_name,
            room_reservation_name: order.room_reservation_name,
            party_reservation_name: order.party_reservation_name,
            boat_management_name: order.boat_management_name,
            number_of_person: order.number_of_person,
            member_code,
            member_name,
            guest_name,
            client_customer: order.client_customer,
            lines: orderlines,
            date: now.toLocaleDateString(),
            time: now.toLocaleTimeString(),
        };

        const html = renderToString("KotReceiptTemplate", {
            receipt: receiptData,
        });
         console.log("testt");
        this.printKot(html);
    }

    printKot(html) {
        const printWindow = window.open("", "");

        printWindow.document.write(`
            <html>
                <head>
                    <title>KOT</title>
                    <style>
                        @page {
                            size:80mm auto;
                            margin:3mm;
                        }
                        body{
                            width:80mm;
                            margin:0;
                            font-family:monospace;
                            font-size:12px;
                        }
                        table{
                            width:100%;
                            border-collapse:collapse;
                        }
                        td{
                            padding:2px 0;
                        }
                        h3{
                            text-align:center;
                        }
                    </style>
                </head>
                <body>
                    ${html}
                </body>
            </html>
        `);

        printWindow.document.close();
        printWindow.focus();
        printWindow.print();
        printWindow.close();
    }
}
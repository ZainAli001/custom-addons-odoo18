/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { renderToString } from "@web/core/utils/render";

patch(ControlButtons.prototype, {
    async onClickKot() {
        const order = this.pos.get_order();
        if (!order) {
            return;
        }
//        const receipt_num = {
//            order_number: order.name,
//
//        };
        const customer = order.get_partner();

        const orderlines = order.get_orderlines().map(line => ({
            product_name: line.get_product().display_name,
            full_product_name: line.get_full_product_name(),
            qty: line.get_quantity(),
            price: line.get_unit_price(),
            discount: line.get_discount(),
//            note: line.get_note(),
        }));
        console.log("orderlines",orderlines);

        let member_code = "";
        let member_name = "";
        let guest_name = "";

        if (customer) {
                member_name = customer.name;
            }


        const now = new Date();

        const receipt = {
            company_name: this.pos.company.name,
            company_image: this.pos.company_logo_base64,
            order_name: order.name,
            table: order.table?.name || "",

            member_name,
//            client_customer: order.client_customer,
            lines: orderlines,
            date: now.toLocaleDateString(),
            time: now.toLocaleTimeString(),
        };

        console.log("receipt",receipt);
        const html = renderToString("KotReceiptTemplate", {
            receipt,
        });

        console.log("html",html);

        this.printKot(html);
    },

    printKot(html) {
    const printWindow = window.open(
        "",
        "_blank",
        "width=800,height=600,left=200,top=200"
    );

    if (!printWindow) {
        alert("Please allow popups for this site to print.");
        return;
    }

    printWindow.document.open();
    printWindow.document.write(`
        <html>
            <body>
                ${html}
            </body>
        </html>
    `);
    printWindow.document.close();


    printWindow.onload = function () {
        setTimeout(() => {
            printWindow.focus();
            printWindow.print();
            printWindow.close();
        }, 250);
    };


},
});
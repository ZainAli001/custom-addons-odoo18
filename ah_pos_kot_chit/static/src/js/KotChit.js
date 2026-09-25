odoo.define('ah_pos_kot_chit.KotChitButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');
    const core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;

    class KotChitButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this._onClick);
        }
        async _onClick(){
            const order = this.env.pos.get_order();
            if (!order) return;
            const customer = order.get_client();
            const orderlines = order.get_orderlines().map(line => ({
                product_name: line.get_product().display_name,
                qty: line.get_quantity(),
                price: line.get_unit_price(),
                discount: line.get_discount(),
                note: line.get_note(),
            }));
            var member_code = '';
            var member_name = '';
            var guest_name = '';
            if(customer) {
                let partner = this.env.pos.db.get_partner_by_id(customer.id)
                if(partner) {
                    if(partner.parent_partner_id) {
                        guest_name = partner.name
                        member_name = partner.parent_partner_id ? partner.parent_partner_id[1]: ''
                        member_code = partner.membership_no
                    }
                    else{
                        guest_name = ''
                        member_name = partner.name
                        member_code = partner.membership_no
                    }
                }
            }
            var d = new Date();
            var date = `${String(d.getDate()).padStart(2, '0')}-${String(d.getMonth() + 1).padStart(2, '0')}-${d.getFullYear()}`;
            var receiptData = {
                company_name: order.pos.company.name,
                company_image: order.pos.company_logo_base64,
                order_name: order.name,
                table: order.table ? order.table.name : '',
                waiter_name: order.waiter_name,
                room_reservation_name: order.room_reservation_name,
                party_reservation_name: order.party_reservation_name,
                boat_management_name: order.boat_management_name,
                number_of_person: order.number_of_person,
                member_code: member_code,
                member_name: member_name,
                guest_name: guest_name,
                client_customer: order.client_customer,
                lines: orderlines,
                date: date,
                time: moment().format('HH:mm'),
            };
            const html = QWeb.render('KotReceiptTemplate', {
                receipt: receiptData,
            });
            this.printKot(html);
        }

        printKot(html) {
            const printWindow = window.open('', '');
            printWindow.document.write(`
                <html>
                <head>
                    <title>KOT</title>
                    <style>
                        @page {
                            size: 80mm auto;
                            margin: 3mm;
                        }

                        body {
                            width: 80mm;
                            margin: 0;
                            font-family: monospace;
                            font-size: 12px;
                        }

                        table {
                            width: 100%;
                            border-collapse: collapse;
                        }

                        td {
                            padding: 2px 0;
                        }

                        h3 {
                            text-align: center;
                            margin: 4px 0;
                        }

                        hr {
                            border-top: 1px dashed #000;
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

    KotChitButton.template = 'ah_pos_kot_chit.KotChitButton';

    ProductScreen.addControlButton({
        component: KotChitButton,
        condition: () => true,
        position: ['before', 'SetPricelistButton'],
    });

    Registries.Component.add(KotChitButton);
    return KotChitButton;
});

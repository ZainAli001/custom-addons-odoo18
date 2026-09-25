/* @odoo-module  */

import {Component,useState} from "@odoo/owl";
import { registry} from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
//import { rpc } from "@web/core/network/rpc";

export class ListViewAction extends Component{
    static template = "pos_delete_orderline.ListView";

    setup() {
//      this.records = [{'id':1},{'id':2}];
        this.records = [];
        this.state = useState({
            'records':[],
            'posProductCount': 0 ,
            'posConfigCount': 0,

        });
        this.orm  = useService('orm');
//        this.rpc  = useService('rpc');
        this.loadRecords();
        this.loadProductCount();
        this.loadPosConfigCount();

    };

    async loadRecords() {
           const posData = await this.orm.searchRead("pos.order",[],[]);
           console.log("posData",posData);
           this.state.records = posData;
    };

//      async loadRecords() {
//           const posData = await this.rpc('/web/dataset/call_kw/',{
//                model:'pos.orders',
//                method: "search_read",
//                args: [[]],
//                kwargs : {fields : ['pos_reference','amount_total'] },
//           });
//    };

    async loadProductCount() {
    const count = await this.orm.searchCount("product.product", [
        ["available_in_pos", "=", true]
    ]);

    this.state.posProductCount = count;
}


     async loadPosConfigCount() {
            const count = await this.orm.searchCount("pos.config", []);
            this.state.posConfigCount = count;
        };

     get totalRevenue() {
        return  Math.round(
          this.state.records.reduce(
            (total, record) => total + (record.amount_total || 0),
            0
        )
    );

};

}
registry.category('actions').add("pos_delete_orderline.action_list_view",ListViewAction);
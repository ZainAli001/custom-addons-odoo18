/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";

export class RoomPopup extends Component {
    static template = "za_pos_customization.RoomPopup";
    static components = { Dialog };
    static props = {
        close: { type: Function },
        getPayload: { type: Function, optional: true },
        title: { type: String, optional: true },
    };
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            rooms: [],
        });
        this.loadRooms();
    }
    async loadRooms() {
        try {
            const rooms = await this.orm.searchRead(
                "hotel.reservation",
                [["status", "=", "checked_in"]],
                ["id","room_id", "status","guest_id"]
            );
            this.state.rooms = rooms;
            console.log("State rooms:", this.state.rooms);
        } catch (error) {
            console.error("Error loading rooms:", error);
        }
    }
    selectRoom(room) {
        console.log("Selected room:", room);
        this.props.getPayload(room);
        this.props.close(room.id);
    }
    cancel() {
        console.log("Popup cancelled");
        this.props.close(false);
    }
}
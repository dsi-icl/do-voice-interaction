import io from "socket.io-client";
import {addResponse, changeStatus} from "./media";
import {PlayerStatus} from "./const";

export function setupSocket(backendUrl, dispatch) {
    window.socket = io(backendUrl);

    window.socket.on("connect", () => console.log("Socket connected ..."));
    window.socket.on("broad", (data) => dispatch(addResponse(data)));
    window.socket.on("disconnect", () => console.log("Socket disconnected ..."));
}

export function submitRecording(action) {
    return dispatch => {
        window.socket.emit("messages", action);
        dispatch(changeStatus({status: PlayerStatus.PROCESSING}));
    };
}
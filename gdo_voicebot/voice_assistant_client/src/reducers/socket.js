import io from "socket.io-client";

import {v4 as uuidv4} from "uuid";

import {addResponse, changeStatus} from "./media";
import {PlayerStatus} from "./const";

export function setupSocket(backendUrl, dispatch) {
    window.socket = io(backendUrl);

    window.socket.on("connect", () => console.log("Socket connected ..."));
    window.socket.on("response", (data) => {
        console.log("received", data)
      
        dispatch(addResponse({
            ...data,
            id: data.id || uuidv4(),
            date: data.date || new Date()
        }));
    });
    window.socket.on("disconnect", () => console.log("Socket disconnected ..."));
}

export function submitRecording(payload) {
    return dispatch => {
        window.socket.emit("audio-command", {
            type: "audio",
            ...payload,
            id: payload.id || uuidv4(),
            date: payload.date || new Date()
        });
        dispatch(changeStatus({status: PlayerStatus.PROCESSING}));
    };
}

export function submitCommand(payload) {
    return dispatch => {
        window.socket.emit("text-command", {
            type: "command",
            ...payload,
            id: payload.id || uuidv4(),
            date: payload.date || new Date()
        });
        dispatch(changeStatus({status: PlayerStatus.PROCESSING}));
    };
}
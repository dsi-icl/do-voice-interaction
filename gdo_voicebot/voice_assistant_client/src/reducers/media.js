import {createSlice} from "@reduxjs/toolkit";
import {PlayerStatus} from "./const";

export const media = createSlice({
    name: "media",
    initialState: {
        status: PlayerStatus.IDLE,
        responseList: [],
        audio: null
    },
    reducers: {
        changeStatus: (state, action) => {
            state.status = action.payload.status;
        },
        addResponse: (state, action) => {
            state.responseList = [{
                id: action.payload.id,
                date: action.payload.date,
                command: action.payload.command,
                emotion: action.payload.emotion,
                grammar_response: action.payload.grammar_response,
                grammar_message: action.payload.grammar_message,
                response: action.payload.response,
                error: action.payload.error
            }, ...state.responseList];
            state.audio = createDataUrl(action.payload.audio);
            if (!state.audio) {
                state.status = PlayerStatus.IDLE;
            }
        },
        clearAudio: (state) => {
            state.status = PlayerStatus.IDLE;
            state.audio = null;
        },
    },
});

export const {changeStatus, addResponse, clearAudio} = media.actions;

export const selectStatus = state => state.media.status;
export const selectResponses = state => state.media.responseList;
export const selectAudio = state => state.media.audio;

export default media.reducer;

// utilities
function createDataUrl(audio) {
    return (audio && audio.data) ? `data:${audio.contentType};base64,${audio.data}` : null;
}
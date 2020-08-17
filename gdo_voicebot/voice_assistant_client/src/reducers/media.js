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
            state.responseList = [...state.responseList, {
                id: action.payload.id,
                date: action.payload.date,
                command: action.payload.command,
                response: action.payload.response,
                error: action.payload.error
            }];
            state.audio = action.payload.audio ? action.payload.audio : null;
            console.log('Response',state.audio)
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

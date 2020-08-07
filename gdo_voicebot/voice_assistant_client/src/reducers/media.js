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
            state.responseList = [...state.responseList, {text: action.payload.text, error: action.payload.error}];
            state.audio = action.payload.audio.data;
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

import {createSlice} from "@reduxjs/toolkit";

export const media = createSlice({
    name: "media",
    initialState: {
        status: "",
        actions: []
    },
    reducers: {
        changeStatus: (state, action) => {
            console.log("change status", action)
            state.status = action.payload.status;
        },
        addAction:(state, action) => {
            state.actions = [...state.actions, action.payload];
        }
    },
});

export const {changeStatus, addAction} = media.actions;

export const selectStatus = state => state.media.status;
export const selectActions = state => state.media.actions;

export default media.reducer;

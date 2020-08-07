import RecordRTC, {StereoAudioRecorder} from "recordrtc";

import {configureStore} from "@reduxjs/toolkit";

import mediaReducer from "./reducers/media";

export function setupStore() {
    return configureStore({
        reducer: {
            media: mediaReducer,
        },
    });
}

export function setupAudioRecorder() {
    navigator.mediaDevices.getUserMedia({video: false, audio: true}).then(stream => {
        window.stream = stream;

        window.recorder = RecordRTC(stream, {
            recorderType: StereoAudioRecorder,
            type: "audio",
            mimeType: "audio/wav",
            numberOfAudioChannels: 1,
            desiredSampRate: 16000,
        });
    });

}
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
    let streamPromise;
    if (window.audioStream) {
        streamPromise = Promise.resolve(window.audioStream);
    } else {
        streamPromise = navigator.mediaDevices.getUserMedia({video: false, audio: true}).then(stream => {
            window.audioStream = stream;
            return stream;
        });
    }

    return streamPromise.then(stream =>
        RecordRTC(stream, {
            recorderType: StereoAudioRecorder,
            type: "audio",
            mimeType: "audio/wav",
            numberOfAudioChannels: 1,
            desiredSampRate: 16000,
        })
    );
}
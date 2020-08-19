import RecordRTC, {StereoAudioRecorder} from "recordrtc";
import hark from "hark";

import {configureStore} from "@reduxjs/toolkit";

import mediaReducer from "./reducers/media";

export function setupStore() {
    return configureStore({
        reducer: {
            media: mediaReducer,
        },
    });
}

function setupStream() {
    if (window.audioStream) {
        return Promise.resolve(window.audioStream);
    } else {
        return navigator.mediaDevices.getUserMedia({video: false, audio: true}).then(stream => {
            window.audioStream = stream;
            return stream;
        });
    }
}

export function setupAudioRecorder() {
    return setupStream().then(stream =>
        RecordRTC(stream, {
            recorderType: StereoAudioRecorder,
            type: "audio",
            mimeType: "audio/wav",
            numberOfAudioChannels: 1,
            desiredSampRate: 16000,
        })
    );
}

export function setupHark() {
    return setupStream().then(stream => hark(stream, {play: false}));
}

export function replaceHtmlElements(text) {
    return text.replace(/\n/gi, "<br />");
}
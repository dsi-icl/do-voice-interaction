import React, {useCallback} from "react";
import {useDispatch, useSelector} from "react-redux";

import Loader from "react-loader-spinner";
import {Button, Card, Icon} from "semantic-ui-react";

import {changeStatus, selectStatus} from "../reducers/media";
import {submitRecording} from "../reducers/socket";

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import "./SimpleRecorder.css";

const SimpleRecorder = () => {
    const status = useSelector(selectStatus);
    const dispatch = useDispatch();

    const onRecordClick = useCallback(() => {
        dispatch(changeStatus({status: "listening"}));
        window.recorder.clearRecordedData();
        window.recorder.startRecording();
    }, [dispatch]);

    const onStopClick = useCallback(() => {
        window.recorder.stopRecording(() => {
            window.recorder.getDataURL(function (audioDataURL) {
                dispatch(submitRecording({
                    audio: {
                        type: window.recorder.getBlob().type || "audio/wav",
                        sampleRate: window.recorder.sampleRate,
                        bufferSize: window.recorder.bufferSize,
                        data: audioDataURL
                    }
                }));
            });
        });
    }, [dispatch]);

    return <Card centered>
        <Loader type="Bars" color={loaderColor(status)} height={100} width={300}/>
        <Card.Content>
            <Card.Header>{status}</Card.Header>
        </Card.Content>
        <Card.Description>
            <Button.Group className="toolbar-margin">
                <Button icon onClick={onRecordClick}>
                    <Icon name="record" color={recordColor(status)}/>
                </Button>
                <Button icon onClick={onStopClick}>
                    <Icon name="stop" color="red"/>
                </Button>
            </Button.Group>
        </Card.Description>
    </Card>;
};

const loaderColor = (status) => {
    switch (status) {
        case "listening":
            return "#21ba45";
        default:
            return "#FFFFFF";
    }
};

const recordColor = (status) => {
    switch (status) {
        case "listening":
            return "green";
        default:
            return null;
    }
};

export default SimpleRecorder;
import React from "react";
import PropTypes from "prop-types";
import {connect} from "react-redux";
import {Button, Icon} from "semantic-ui-react";

import {changeStatus, hotwordResponse, foundHotword} from "../reducers/media";
import {submitHotwordRecording, submitRecording} from "../reducers/socket";
import {setupAudioRecorder, setupHark} from "../util";
import {PlayerStatus} from "../reducers/const";

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import "./SimpleRecorder.css";

class SimpleRecorder extends React.Component {
    constructor(props) {
        super(props);

        this.state = {recorder: null, hark: null, backgroundRecorder: null, backgroundHark: null};
    }

    componentDidMount() {
        this.listenForHotword()
    }

    componentDidUpdate(prevProps) {
        if (prevProps.receivedHotwordRes != this.props.receivedHotwordRes) {
            if (this.props.detectedHotword) {
                this.onRecordClick()
                this.props.dispatch(foundHotword(false));
            } else {
                this.listenForHotword()
            }

            this.props.dispatch(hotwordResponse(false));
        }
    }

    listenForHotword() {
        if (this.props.status === PlayerStatus.IDLE) {
            if (this.state.backgroundRecorder) {
                this.state.backgroundRecorder.destroy();
                this.setState({backgroundRecorder: null});
            }

            setupAudioRecorder().then(backgroundRecorder => {
                this.setState({backgroundRecorder});
                backgroundRecorder.clearRecordedData();
                backgroundRecorder.startRecording();
            });

            setupHark().then(backgroundHark => {
                this.setState({backgroundHark});
                backgroundHark.on("speaking", () => {
                    console.log("Hotword speaking");
                });

                backgroundHark.on("stopped_speaking", () => {
                    console.log("Hotword stopped talking");
                    this.sendHotwordRecording()
                });
            });
        }
    }

    sendHotwordRecording() {
        if (this.props.status === PlayerStatus.IDLE && this.state.backgroundRecorder) {
            this.state.backgroundRecorder.stopRecording(() => {
                this.state.backgroundRecorder.getDataURL((audioDataURL) => {
                    submitHotwordRecording({
                        audio: {
                            type: this.state.backgroundRecorder.getBlob().type || "audio/wav",
                            sampleRate: this.state.backgroundRecorder.sampleRate,
                            bufferSize: this.state.backgroundRecorder.bufferSize,
                            data: audioDataURL.split(",").pop()
                        }
                    })
                });
            });
        }

    }

    onRecordClick() {
        if (this.props.status === PlayerStatus.IDLE) {
            this.props.dispatch(changeStatus({status: PlayerStatus.LISTENING}));
            if (this.state.recorder) {
                this.state.recorder.destroy();
                this.setState({recorder: null});
            }

            setupAudioRecorder().then(recorder => {
                this.setState({recorder});
                recorder.clearRecordedData();
                recorder.startRecording();
            });

            if (this.state.hark) {
                this.state.hark.stop();
                this.setState({hark: null});
            }

            setupHark().then(hark => {
                this.setState({hark});
                hark.on("speaking", () => {
                    console.log("speaking");
                });

                hark.on("stopped_speaking", () => {
                    console.log("stopped talking");
                    this.onStopClick();
                });
            });
        }
    }

    onStopClick() {
        if (this.props.status === PlayerStatus.LISTENING && this.state.recorder) {
            this.state.recorder.stopRecording(() => {
                this.state.recorder.getDataURL((audioDataURL) => {
                    this.props.dispatch(submitRecording({
                        audio: {
                            type: this.state.recorder.getBlob().type || "audio/wav",
                            sampleRate: this.state.recorder.sampleRate,
                            bufferSize: this.state.recorder.bufferSize,
                            data: audioDataURL.split(",").pop()
                        }
                    }));
                });
            });
        }

        if (this.state.hark) {
            this.state.hark.stop();
        }

        this.listenForHotword()
    }

    recordColor(status) {
        switch (status) {
            case PlayerStatus.LISTENING:
                return "green";
            default:
                return null;
        }
    }

    render() {
        return <Button.Group className="toolbar-margin">
            <Button icon onClick={this.onRecordClick.bind(this)} disabled={this.props.status !== PlayerStatus.IDLE}>
                <Icon name="record" color={this.recordColor(this.props.status)}/>
            </Button>
            <Button icon onClick={this.onStopClick.bind(this)} disabled={this.props.status !== PlayerStatus.LISTENING}>
                <Icon name="stop" color="red"/>
            </Button>
        </Button.Group>;
    }
}

SimpleRecorder.propTypes = {
    status: PropTypes.string,
    dispatch: PropTypes.func
};

const mapStateToProps = state => ({status: state.media.status, receivedHotwordRes: state.media.receivedHotwordRes, detectedHotword: state.media.detectedHotword});

export default connect(mapStateToProps)(SimpleRecorder);
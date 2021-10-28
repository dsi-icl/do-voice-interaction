import React from "react";
import PropTypes from "prop-types";
import {connect} from "react-redux";
import {Button, Icon} from "semantic-ui-react";

import {changeStatus} from "../reducers/media";
import {submitRecording} from "../reducers/socket";
import {setupAudioRecorder, setupHark} from "../util";
import {PlayerStatus} from "../reducers/const";

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import "./SimpleRecorder.css";

class SimpleRecorder extends React.Component {
    constructor(props) {
        super(props);

        this.state = {recorder: null, hark: null};
    }

    onHotwordClick() {
        if (this.props.status === PlayerStatus.OFF) {
            this.props.dispatch(changeStatus({status: PlayerStatus.IDLE}));

            if (this.state.recorder) {
                this.state.recorder.destroy();
                this.setState({recorder: null});
            }

            setupAudioRecorder().then(recorder => {
                this.setState({recorder});
                recorder.clearRecordedData();
                recorder.startRecording();
            });

            setupHark().then(hark => {
                this.setState({hark});
                hark.on("speaking", () => {
                    console.log("Hotword speaking");
                });

                hark.on("stopped_speaking", () => {
                    console.log("Hotword stopped talking");
                    // TODO send data to hotword service
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
            <Button icon onClick={this.onHotwordClick.bind(this)} disabled={this.props.status !== PlayerStatus.OFF}>
                <Icon name="fire" color="orange"/>
            </Button>
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

const mapStateToProps = state => ({status: state.media.status});

export default connect(mapStateToProps)(SimpleRecorder);
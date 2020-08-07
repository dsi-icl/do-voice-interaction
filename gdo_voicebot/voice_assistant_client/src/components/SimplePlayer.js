import React from "react";
import {useDispatch, useSelector} from "react-redux";

import ReactAudioPlayer from "react-audio-player";

import {changeStatus, clearAudio, selectAudio} from "../reducers/media";
import {PlayerStatus} from "../reducers/const";


const SimpleRecorder = () => {
    const audio = useSelector(selectAudio);
    const dispatch = useDispatch();

    return <ReactAudioPlayer src={audio} autoPlay onEnded={() => dispatch(clearAudio())}
                             onPlay={() => dispatch(changeStatus({status: PlayerStatus.RESPONDING}))}/>;
};

export default SimpleRecorder;
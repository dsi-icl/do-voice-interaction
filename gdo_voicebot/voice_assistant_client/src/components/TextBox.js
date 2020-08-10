import React, {useCallback, useState} from "react";
import {useDispatch} from "react-redux";

import {Button, Icon, Input} from "semantic-ui-react";

import {submitCommand} from "../reducers/socket";
import {changeStatus} from "../reducers/media";
import {PlayerStatus} from "../reducers/const";

const TextBox = () => {
    const [message, setMessage] = useState("");

    const dispatch = useDispatch();

    const handleSubmit = useCallback(() => {
        dispatch(submitCommand({command: message}));
        setMessage("");
    }, [message, setMessage, dispatch]);

    const handleChange = useCallback((e, {value}) => {
        setMessage(value);
        if (value && value.length > 0) {
            dispatch(changeStatus({status: PlayerStatus.TYPING}));
        } else {
            dispatch(changeStatus({status: PlayerStatus.IDLE}));
        }
    }, [setMessage, dispatch]);

    return <Input type="text" placeholder="command" fluid action value={message} onChange={handleChange}>
        <input/>
        <Button icon onClick={handleSubmit}><Icon name="chat"/></Button>
    </Input>;
};

export default TextBox;
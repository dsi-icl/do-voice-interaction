import React from "react";
import {useSelector} from "react-redux";

import Loader from "react-loader-spinner";
import {Card, Container} from "semantic-ui-react";

import SimpleRecorder from "../components/SimpleRecorder";
import SimplePlayer from "../components/SimplePlayer";

import {selectStatus} from "../reducers/media";
import {PlayerStatus} from "../reducers/const";

const App = () => {
    return <Container>
        <Card centered>
            <StatusBar/>
            <Card.Description>
                <SimpleRecorder/>
            </Card.Description>
        </Card>
        <SimplePlayer/>
    </Container>;
};

const StatusBar = () => {
    const status = useSelector(selectStatus);

    return <>
        <Loader type="Bars" color={loaderColor(status)} height={100} width={300}/>
        <Card.Content>
            <Card.Header>{status}</Card.Header>
        </Card.Content>
    </>;
};

const loaderColor = (status) => {
    switch (status) {
        case PlayerStatus.LISTENING:
            return "#21ba45";
        default:
            return "#FFFFFF";
    }
};

export default App;

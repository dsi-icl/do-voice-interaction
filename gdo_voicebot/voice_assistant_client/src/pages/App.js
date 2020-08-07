import React from "react";
import {useSelector} from "react-redux";

import {Card, Container} from "semantic-ui-react";

import {selectActions, selectStatus} from "../reducers/media";
import SimpleRecorder from "../components/SimpleRecorder";
import Loader from "react-loader-spinner";

function App() {
    const status = useSelector(selectStatus);
    const actions = useSelector(selectActions);

    console.log("status", status);
    console.log("actions", actions);

    return <Container>
        <Card centered>
            <Loader type="Bars" color={loaderColor(status)} height={100} width={300}/>
            <Card.Content>
                <Card.Header>{status}</Card.Header>
            </Card.Content>
            <Card.Description>
                <SimpleRecorder/>
            </Card.Description>
        </Card>
    </Container>;
}

const loaderColor = (status) => {
    switch (status) {
        case "listening":
            return "#21ba45";
        default:
            return "#FFFFFF";
    }
};

export default App;

import React from "react";
import {useSelector} from "react-redux";

import Loader from "react-loader-spinner";
import {Container, Grid} from "semantic-ui-react";

import SimpleRecorder from "../components/SimpleRecorder";
import SimplePlayer from "../components/SimplePlayer";
import TextBox from "../components/TextBox";
import CommandFeed from "../components/CommandFeed";
import { HumanThayers, BotThayers } from "../components/ThayersCharts";

import {selectStatus} from "../reducers/media";
import {PlayerStatus} from "../reducers/const";

import "./App.css";



const App = () => {
    return <Container>
        <div className="center main-div">
            <Grid>
                <StatusBar/>
                <Grid.Row>
                    <Grid.Column width={13}>
                        <TextBox/>
                    </Grid.Column>
                    <Grid.Column width={3}>
                        <SimpleRecorder/>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column width={16}>
                        <SimplePlayer/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
            <CommandFeed/>
        </div>
        <div className="left">
            <HumanThayers/>
        </div>
        <div className="right">
            <BotThayers/>
        </div>
        
    </Container>;
};

const StatusBar = () => {
    const status = useSelector(selectStatus);

    return <>
        <Grid.Row>
            <Grid.Column width={16}>
                <Loader type="Bars" color={loaderColor(status)} height={100} width={550}/>
            </Grid.Column>
        </Grid.Row>
        <Grid.Row>
            <Grid.Column width={16}>
                <h3>Status: {status}</h3>
            </Grid.Column>
        </Grid.Row>
    </>;
};

const loaderColor = (status) => {
    switch (status) {
        case PlayerStatus.LISTENING:
        case PlayerStatus.TYPING:
            return "#FFFFFF";
        case PlayerStatus.PROCESSING:
            return "#FF4500";
        case PlayerStatus.RESPONDING:
            return "#FFA500";
        default:
            return "#FFFFFF00";
    }
};

export default App;

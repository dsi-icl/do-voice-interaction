import React from "react";
import PropTypes from "prop-types";

import {Feed, Icon} from "semantic-ui-react";
import {useSelector} from "react-redux";

import parse from "html-react-parser";

import {selectResponses} from "../reducers/media";
import {replaceHtmlElements} from "../util";

import "./CommandFeed.css";

const CommandFeed = () => {
    const responses = useSelector(selectResponses);
    return <Feed className="feed-text">
        {responses.map(e => <FeedItem key={e.id} date={e.date} command={e.command} emotion={e.emotion} response={e.response} error={e.error}/>)}
    </Feed>;
};

const FeedItem = ({date, command, emotion, response, error}) => <Feed.Event>
    <Feed.Label>
        <Icon name="comments" className="feed-icon"/>
    </Feed.Label>
    <Feed.Content>
        <Feed.Date className="feed-text">{date}</Feed.Date>
        <Feed.Summary className="feed-text">You: {parse(replaceHtmlElements(command))}</Feed.Summary>
        <Feed.Summary className="feed-text">Emotion Detected: {parse(replaceHtmlElements(emotion))}</Feed.Summary>
        {response && <Feed.Extra text className="feed-text">Assistant: {parse(replaceHtmlElements(response))}</Feed.Extra>}
        {error && <Feed.Extra text className="feed-text-error">Error: {parse(replaceHtmlElements(error))}</Feed.Extra>}
    </Feed.Content>
</Feed.Event>;

FeedItem.propTypes = {
    date: PropTypes.string,
    command: PropTypes.string,
    emotion: PropTypes.string,
    response: PropTypes.string,
    error: PropTypes.string,
};

export default CommandFeed;
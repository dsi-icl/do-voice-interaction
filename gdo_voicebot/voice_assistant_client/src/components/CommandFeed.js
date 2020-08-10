import React from "react";
import PropTypes from "prop-types";

import {Feed, Icon} from "semantic-ui-react";
import {useSelector} from "react-redux";

import {selectResponses} from "../reducers/media";

import "./CommandFeed.css";

const CommandFeed = () => {
    const responses = useSelector(selectResponses);
    return <Feed className="feed-text">
        {responses.map(e => <FeedItem key={e.id} date={e.date} command={e.command} response={e.response} error={e.error}/>)}
    </Feed>;
};

const FeedItem = ({date, command, response, error}) => <Feed.Event>
    <Feed.Label>
        <Icon name="comments" className="feed-icon"/>
    </Feed.Label>
    <Feed.Content>
        <Feed.Date className="feed-text">{date}</Feed.Date>
        <Feed.Summary className="feed-text">You: {command}</Feed.Summary>
        <Feed.Extra text className="feed-text">Assistant: {response}</Feed.Extra>
        <Feed.Extra text className="feed-text-error">Error: {error}</Feed.Extra>
    </Feed.Content>
</Feed.Event>;

FeedItem.propTypes = {
    date: PropTypes.string,
    command: PropTypes.string,
    response: PropTypes.string,
    error: PropTypes.string,
};

export default CommandFeed;
import React from "react";
import PropTypes from "prop-types";

import {Feed, Icon} from "semantic-ui-react";
import {useSelector} from "react-redux";

import ReactHtmlParser from "react-html-parser";

import {selectResponses} from "../reducers/media";
import {replaceHtmlElements} from "../util";

import "./CommandFeed.css";

const CommandFeed = () => {
    const responses = useSelector(selectResponses);
    return <Feed className="feed-text">
        {responses.map(e => <FeedItem key={e.id} date={e.date} command={e.command} emotion={e.emotion} grammar_response={e.grammar_response} grammar_message={e.grammar_message} response={e.response} error={e.error}/>)}
    </Feed>;
};

function messageColor(index, positions) {
    if (positions.includes(index)) {
        return "red"
    }
    return "white"
}

const FeedItem = ({date, command, emotion, grammar_response, grammar_message, response, error}) => <Feed.Event>
    <Feed.Label>
        <Icon name="comments" className="feed-icon"/>
    </Feed.Label>
    <Feed.Content>
        <Feed.Date className="feed-text">{date}</Feed.Date>
        <Feed.Summary className="feed-text">You: {ReactHtmlParser(replaceHtmlElements(command))}</Feed.Summary>
        <Feed.Summary className="feed-text">Emotion Detected: {ReactHtmlParser(replaceHtmlElements(emotion))}</Feed.Summary>
        <Feed.Summary className="feed-text">Grammar Correction output:</Feed.Summary>
        <div>
            {grammar_message.split(" ").map((word, index) => {
                return <span style={{ color: messageColor(index, grammar_response) }}>{`${word} `}</span>;
            })}
        </div>
        {response && <Feed.Extra text className="feed-text">Assistant: {ReactHtmlParser(replaceHtmlElements(response))}</Feed.Extra>}
        {error && <Feed.Extra text className="feed-text-error">Error: {ReactHtmlParser(replaceHtmlElements(error))}</Feed.Extra>}
    </Feed.Content>
</Feed.Event>;

FeedItem.propTypes = {
    date: PropTypes.string,
    command: PropTypes.string,
    emotion: PropTypes.string,
    grammar_response: PropTypes.array,
    grammar_message: PropTypes.string,
    response: PropTypes.string,
    error: PropTypes.string,
};

export default CommandFeed;
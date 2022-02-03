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
        {responses.map(e => <FeedItem key={e.id} date={e.date} command={e.command} emotion={e.emotion} grammar_positions={e.grammar_positions} grammar_prediction={e.grammar_prediction} response={e.response} error={e.error}/>)}
    </Feed>;
};

function messageColor(index, positions) {
    if (positions.includes(index)) {
        return "red"
    }
    return "white"
}

const FeedItem = ({date, command, emotion, grammar_positions, grammar_prediction, response, error}) => <Feed.Event>
    <Feed.Label>
        <Icon name="comments" className="feed-icon"/>
    </Feed.Label>
    <Feed.Content>
        <Feed.Date className="feed-text">{date}</Feed.Date>
        <Feed.Summary className="feed-text">You: {parse(replaceHtmlElements(command))}</Feed.Summary>
        <Feed.Summary className="feed-text">Emotion Detected: {parse(replaceHtmlElements(emotion))}</Feed.Summary>
        {grammar_prediction && <Feed.Summary className="feed-text">Grammar Correction output:</Feed.Summary>}
        {grammar_prediction && <div>
            {command.split(" ").map((word, index) => {
                return <span style={{ color: messageColor(index, grammar_positions) }}>{`${word} `}</span>;
            })}
        </div>}
        {grammar_prediction && <Feed.Summary className="feed-text">Correction: {parse(replaceHtmlElements(grammar_prediction))}</Feed.Summary>}
        {response && <Feed.Extra text className="feed-text">Assistant: {parse(replaceHtmlElements(response))}</Feed.Extra>}
        {error && <Feed.Extra text className="feed-text-error">Error: {parse(replaceHtmlElements(error))}</Feed.Extra>}
    </Feed.Content>
</Feed.Event>;

FeedItem.propTypes = {
    date: PropTypes.string,
    command: PropTypes.string,
    emotion: PropTypes.string,
    grammar_positions: PropTypes.array,
    grammar_prediction: PropTypes.string,
    response: PropTypes.string,
    error: PropTypes.string,
};

export default CommandFeed;
import express from "express";
import cors from "cors";
import logger from "morgan";
import fs from "fs";

if (!fs.existsSync("./config/config.json")) {
    console.error("Could not find the configuration file: './config/config.json'");
    process.exit(1);
}

global.config = JSON.parse(fs.readFileSync("./config/config.json").toString());

const app = express();

app.use(cors());
app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({extended: false}));

import {speech_to_text, getAudio} from "./routes/stt.js";

getAudio();

app.get("/deepspeech/text-message", function(req,res) {

    let result = speech_to_text("./src/audio/test.wav");
    console.log(result);
    res.send(result);

});

export default app;

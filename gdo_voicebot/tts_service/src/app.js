import express from "express";
import cors from "cors";
import logger from "morgan";
import fs from "fs";
import axios from "axios";

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

import {sampleData} from "./routes";
import {generate_voice_message} from "./routes/tts.js";

app.get("/api/status", (req, res) => res.send("Service is running"));
app.get("/api/json", sampleData);

app.get("/gtts/audio", (req, res) => {

    axios.get("http://localhost:4000/voice-assistant/text-answer").then(function (response) {
        console.log(response.data);
        generate_voice_message(response.data);
    });

    res.send("done");

});
export default app;

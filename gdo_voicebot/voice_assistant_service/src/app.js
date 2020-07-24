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

import {sampleData} from "./routes";

app.get("/api/status", (req, res) => res.send("Service is running"));
app.get("/api/json", sampleData);

app.get("/voice-assistant/record",(req,res) => res.download("./src/audio/show_me_paris.wav"), function (err) {
    console.log(err);
});

var bot_message = "Welcome to the GDO";
app.get("/voice-assistant/text-answer", (req,res) => res.send(bot_message));

export default app;

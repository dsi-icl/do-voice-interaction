import express from "express";
import cors from "cors";
import logger from "morgan";
import fs from "fs";
import Gtts from "gtts";

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

app.get("/api/tts", (req, res) => {

    const gtts = new Gtts(req.query.text,req.query.lang);
    gtts.stream().pipe(res);

});

export default app;

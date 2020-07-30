import express from "express";
import cors from "cors";
import logger from "morgan";
import fs from "fs";

if (!fs.existsSync("./config/config.json")) {
    console.error("Could not find the configuration file: './config/config.json'");
    process.exit(1);
}

global.config = JSON.parse(fs.readFileSync("./config/config.json").toString());

import { speech_to_text, loadDeepSpeechModel } from "./routes/stt.js";

const app = express();
try {
    var model = loadDeepSpeechModel();
} catch (error) {
    console.log("Error during deepspeech model construction");
    console.log(error);
}

app.use(cors());
app.use(logger("dev"));
app.use(express.text({ limit: "50mb" }));
app.use(express.urlencoded({ extended: false }));


import { sampleData, isEmpty } from "./routes/index.js";


app.get("/api/status", (req, res) => res.send("Service is running"));
app.get("/api/json", sampleData);
app.post("/api/stt", (req, res) => {

    if (isEmpty(req.body)) {
        //res.statusCode = 400;
        res.json({"status":"fail", "message":"The request body contains nothing"});

    } else {
        const buffer = Buffer.from(req.body, "utf16le");
        const textMessage = speech_to_text(buffer, model);

        console.log("Text message :", textMessage);
        console.log("Message length :", textMessage.length);
        if (textMessage.length == 0) {
            //res.statusCode = 400;
            res.json({"status":"fail", "service": "Speech To Text service","message": "no transcription for this"});
        } else {
            //res.statusCode = 200;
            res.json({"status":"ok","text":textMessage});
        }
    }

});

export default app;

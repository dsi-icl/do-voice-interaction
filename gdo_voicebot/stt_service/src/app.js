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
app.use(express.text({limit:"50mb"}));
app.use(express.urlencoded({extended: false}));

//import {speech_to_text, getAudio} from "./routes/stt.js";

import {sampleData,isEmpty} from "./routes/index.js";

app.get("/api/status", (req, res) => res.send("Service is running"));
app.get("/api/json", sampleData);
app.post("/api/stt", (req,res) => {

    if(isEmpty(req.body)){
        res.statusCode=400;
        res.json({"status":"fail","message":"The request body contains nothing"});
    } else {
        /* const buffer = req.body; */
        res.json({"status":"ok","text":"Not implemented yet"});
    }

    
});

export default app;

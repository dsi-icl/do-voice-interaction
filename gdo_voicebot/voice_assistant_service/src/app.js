import express from "express";
import cors from "cors";
import logger from "morgan";
import fs from "fs";
import http from "http";
import path from "path";
import socketio from "socket.io";
import fetch from "node-fetch";


if (!fs.existsSync("./config/config.json")) {
    console.error("Could not find the configuration file: './config/config.json'");
    process.exit(1);
}

global.config = JSON.parse(fs.readFileSync("./config/config.json").toString());

const app = express();
var httpServer = http.createServer(app);
const __dirname = path.resolve();


app.use(cors());
app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({extended: false}));

import {sampleData} from "./routes/index.js";

app.get("/api/status", (req, res) => res.send("Service is running"));
app.get("/api/json", sampleData);
app.use("/node_modules", express.static(__dirname + "/node_modules"));
app.use("/api/echo", express.static("public"));

httpServer.listen(4000, () => {
    console.log("listening on *:4000");
});

var io = socketio.listen(httpServer);

io.on("connect",(client) =>{

    console.log("Client connected ");

    client.on("message", async function(data) {
        console.log("record done");
        const dataURL = data.audio.dataURL.split(",").pop();

        let fileBuffer = Buffer.from(dataURL, "base64");
        let sttResponse =  await postData("http://localhost:3000/api/stt",fileBuffer);

        if(sttResponse!=null && sttResponse["status"]=="ok"){
            var voiceAnswer = await getData("http://localhost:5000/api/tts","Me gusta el chocolate");
            client.emit("result",voiceAnswer);
        } else {
            console.log("status :",sttResponse["status"]);
            console.log("error message :",sttResponse["message"]);
        }
        
    });
});

async function postData(url, data) {
    let jsondata;
    await fetch(url, {
        method: "post",
        headers: { "Content-type": "text/plain" },
        body: data
    })
        .then(res => res.json())
        .then(json => {
            jsondata = json;
        })
        .catch(error => {
            console.log("Error", error);
            return null;
        });

    return jsondata;
}

async function getData(requestUrl,robotAnswer){

    var url = new URL(requestUrl),
        params = {text:robotAnswer,lang:"es"};
    Object.keys(params).forEach(key =>
        url.searchParams.append(key, params[key]));
    let response = await fetch(url);
    let data = await response.arrayBuffer();

    return data;
}

/* app.get("/voice-assistant/record",(req,res) => res.download("./src/audio/show_me_paris.wav"), function (err) {
    console.log(err);
});

var bot_message = "Welcome to the GDO. Can I help you ?";
app.get("/voice-assistant/text-answer", (req,res) => res.send(bot_message));

import {getAudio} from "./routes/voice_assistant.js";

getAudio();

app.get("voice-assistant/voice-answer", (req,res) => {

    var voice_answer = "./src/audio/voice.wav";

}); */

export default app;

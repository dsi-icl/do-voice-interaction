import express from "express";
import cors from "cors";
import logger from "morgan";
import fs from "fs";
import http from "http";
/* import ss from "socket.io-stream"; */
import path from "path";
import socketio from "socket.io";


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
app.get("/api/echo", (req,res)=> {
    res.sendFile(__dirname +"/public/index.html");
});

app.get("/api/stylesheets/style.css", (req,res)=>{
    res.sendFile(__dirname +"/public/stylesheets/style.css");
});

app.use("/node_modules", express.static(__dirname + "/node_modules"));

httpServer.listen(4000, () => {
    console.log("listening on *:4000");
});

var io = socketio.listen(httpServer);
/* io.of("/api/echo").on("connect",(client) =>{ */
io.on("connect",(client) =>{

    console.log("Client connected ");/* +String.valueOf(client.request.connection) */
    //client.emit("server_setup", "Server connected [id=${client.id}]");
    client.on("message", async function(data) {
        console.log("record done");
        const dataURL = data.audio.dataURL.split(",").pop();
        let fileBuffer = Buffer.from(dataURL, "base64");
        client.emit("test",{"msg":"it's ok"});
    
    });
});

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

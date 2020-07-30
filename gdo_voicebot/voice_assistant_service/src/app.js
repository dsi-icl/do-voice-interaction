import express from "express";
import cors from "cors";
import logger from "morgan";
import fs from "fs";
import http from "http";
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

import {sampleData, postData, getData} from "./routes/index.js";

app.get("/api/status", (req, res) => res.send("Service is running"));
app.get("/api/json", sampleData);
app.use("/node_modules", express.static(__dirname + "/node_modules"));
app.use("/api/echo", express.static("public"));

httpServer.listen(4000, () => {
    console.log("listening on *:4000\n");
});

var io = socketio.listen(httpServer);

io.on("connect",(client) =>{

    console.log("Client connected\n");

    client.on("message", async function(data) {
        console.log("RECORD DONE\n");
        const dataURL = data.audio.dataURL.split(",").pop();
        const fileBuffer = Buffer.from(dataURL,"base64");
        let sttResponse =  await postData("http://localhost:3000/api/stt",dataURL);

        if(sttResponse!=null && sttResponse["status"]=="ok"){
            console.log("Speech to text transcription : SUCCESS\n")
            client.emit("user-request",{"user":sttResponse["text"]});
            var voiceAnswer = await getData("http://localhost:5000/api/tts","The Data Observatory control service has not been integrated yet");
            client.emit("result",voiceAnswer);
            client.emit("robot-answer",{"robot":"The DO control service has not been integrated yet"});
        } else {
            var voiceAnswer = await getData("http://localhost:5000/api/tts","I encountered an error. Please consult technical support or try the request again");
            client.emit("problem",sttResponse);
            client.emit("voice-alert",voiceAnswer);
            client.emit("user-request",{"user":"..."});
            client.emit("robot-answer",{"robot":"I encountered an error. Please consult technical support or try the request again."});
            console.log("Speech to text transcription : FAIL\n");
            console.log("Status :",sttResponse["status"]);
            console.log("Concerned service : ",sttResponse["service"]);
            console.log("Error message :",sttResponse["message"]+"\n");
        }

    });
});

export default app;

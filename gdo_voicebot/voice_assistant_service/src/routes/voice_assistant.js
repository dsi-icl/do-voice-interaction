const Recorder = require("node-record-lpcm16");
const MemoryStream = require("memory-stream");
const Fs = require("fs");
const Axios = require("axios");
var FileWriter = require("wav").FileWriter;

//Function to be used to record the user's request
function record(){

    //We create a binary stream with the name of the file were the record will be saved.
    const file = Fs.createWriteStream("./audio/test.wav", { encoding: "binary" });
    const audioStream = new MemoryStream();

    //DeepSpeech works with 16000Hz/s, monochannel, 16 Bit, wav formats
    const recording = Recorder.record({
        sampleRate: 16000,
        channels: 1,
        audioType: "wav"
    });

    console.log("* Recording");

    // // Pause recording after one second
    // setTimeout(() => {
    //   recording.pause()
    // }, 1000)
    //
    // // Resume another second later
    // setTimeout(() => {
    //   recording.resume()
    // }, 2000)

    recording.stream()
        .on("error", err => {
            console.error("recorder threw an error:", err);
        })
        .pipe(file);

    // Stop recording after five seconds
    setTimeout(() => {
        recording.stop();
        console.log("* End of recording");
    }, 5000);

    return audioStream.toBuffer();

}

/* record(); */

// Function to get an audio file from an API request and save it audio repertory
// This function will be used to get the voice robot answer in a wav file
export async function getAudio() {

    const writer = new FileWriter("./src/audio/voice.wav", {
        sampleRate: 16000,
        channels: 1,
        bitDepth: 16
    });

    const response = await Axios({
        method: "GET",
        url: "http://localhost:5000/gtts/audio",
        responseType: "stream"
    });

    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
        writer.on("finish", resolve);
        writer.on("error", reject);
    });

} 
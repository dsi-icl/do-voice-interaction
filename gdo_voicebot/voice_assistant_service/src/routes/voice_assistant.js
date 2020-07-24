const Recorder = require("node-record-lpcm16");
const MemoryStream = require("memory-stream");
const Fs = require("fs");

function record(){

    const file = Fs.createWriteStream("./audio/test.wav", { encoding: "binary" });
    const audioStream = new MemoryStream();

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

record();

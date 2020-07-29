const Fs = require("fs");
const Axios = require("axios");
var FileWriter = require("wav").FileWriter;
const DeepSpeech = require("deepspeech");

export function speech_to_text(audioFile) {

    const BEAM_WIDTH = 1024;
    let modelPath = "./src/models/deepspeech-0.7.4-models.pbmm";

    let model = new DeepSpeech.Model(modelPath);
    model.setBeamWidth(BEAM_WIDTH);

    const LM_ALPHA = 0.75;
    const LM_BETA = 1.85;
    let scorerPath = "./src/models/deepspeech-0.7.4-models.scorer";

    model.enableExternalScorer(scorerPath);
    model.setScorerAlphaBeta(LM_ALPHA,LM_BETA);

    if (!Fs.existsSync(audioFile)) {
        console.log("file missing:", audioFile);
        process.exit();
    }

    const buffer = Fs.readFileSync(audioFile);
    let result = model.stt(buffer);

    return result;

}

export async function getAudio() {

    const writer = new FileWriter("./src/audio/test.wav", {
        sampleRate: 16000,
        channels: 1,
        bitDepth: 16
    });

    const response = await Axios({
        method: "GET",
        url: "http://localhost:4000/voice-assistant/record",
        responseType: "stream"
    });

    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
        writer.on("finish", resolve);
        writer.on("error", reject);
    });

}

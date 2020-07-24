const gTTS = require("gtts");

export function generate_voice_message(speech){

    let gtts = new gTTS(speech, "en");

    gtts.save("./src/audio/voice.wav", (err) => {
        if(err) { throw new Error(err); }
        console.log("Text to speech converted!");
    });


}

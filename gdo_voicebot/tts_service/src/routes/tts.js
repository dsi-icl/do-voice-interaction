import GTTS from 'gtts'
import { Base64Encode } from 'base64-stream'
import streamToPromise from 'stream-to-promise'

/**
 * Function that execute text to speech service get request
 * @param {Request} req The received request from the voice-assistant service
 * @param {Response} res The response to be sent to the voice-assistant service in stream format
 * @see {@link https://www.npmjs.com/package/gtts|Gtts}
 */
export async function textToSpeech (req, res) {
  try {
    // if using speech fillers then call cereproc speak function
    if (2 === 2) {
      const data = await speakCereProc(req.query.text)
      if (data === '') {
        res.status(400).json({ status: 'fail', service: 'Text To Speech service', error: err.toString() })
      }
      res.status(200).json({ status: 'success', service: 'Text To Speech service', data, contentType: 'audio/wav' })
    } else {
      const data = await speak(getParams(req))
      res.status(200).json({ status: 'success', service: 'Text To Speech service', data, contentType: 'audio/mpeg' })
    }
  } catch (err) {
    res.status(400).json({ status: 'fail', service: 'Text To Speech service', error: err.toString() })
  }
}

function getParams (req) {
  return { text: req.query.text || req.body.text || '', lang: req.query.lang || req.body.lang || 'en-uk' }
}

function speak ({ text, lang }) {
  return streamToPromise(new GTTS(text, lang).stream().pipe(new Base64Encode())).then(data => data.toString())
}

function speakCereProc ({ text }) {
  var fs = require('fs'); 
  fs.open('voice_output.wav', 'w')
  if (textToWav(text, 'voice_output.wav')) {
    return 'voice_output.wav'
  }

  return ''
}

function textToWav(text, output) {
  var config;
  var configTemplate = `{
      "cerevoice_eng": "",
      "voice_file": "",
      "licence_file": "",
      "root_certificate": "",
      "client_certificate":"",
      "client_key":""
  }`
  config = JSON.parse(fs.readFileSync('../../config/config.json', 'utf8'));
  var missing = false;
  if (config.cerevoice_eng == "") {
      console.log("ERROR: missing path to cerevoice_eng.node");
      missing = true;
  }
  if (config.voice_file == "") {
      console.log("ERROR: missing path to voice");
      missing = true;
  }
  if (config.licence_file == "" || config.root_certificate == "" || config.client_certificate == "" || config.client_key == "") {
      console.log("ERROR: missing license info");
      missing = true;
  }
  if (missing) {
      console.log("Please fill in all required config values:\n" + configTemplate + "\nin config.json");
      process.exit(1);
  }


  // Load the voice using the full API
  var eng = config.cerevoice_eng.CPRCEN_engine_load(config.voice_file, config.licence_file, config.root_certificate, config.client_certificate, config.client_key);

  var chan = CPRCEN_engine_open_default_channel(eng);

  var abuf = CPRCEN_engine_channel_speak(eng, chan, txt1, strlen(txt1), 1);
  return CPRC_abuf_wav_data(abuf)

  // if (!eng) {
  //     console.log("ERROR: unable to load voice file '" + voice + "', exiting");
  //     return null;
  // }

  // // Open a channel for voice
  // chan_handle = config.cerevoice_eng.CPRCEN_engine_open_default_channel(eng);
  // if (!chan_handle) {
  //     console.log("ERROR: unable to open default channel, exiting");
  //     return null;
  // }

  // // Set the audio output to a file with WAV format.
  // var res = config.cerevoice_eng.CPRCEN_engine_channel_to_file(eng, chan_handle, output, config.cerevoice_eng.CPRCEN_AUDIO_FORMAT.CPRCEN_RIFF);
  // if (res)
  //     console.log("Text was successfully synthesised and saved to " + output);
  // config.cerevoice_eng.CPRCEN_engine_channel_speak(eng, chan_handle, text + "\n", text.length + 1, 0);
  // // Flush engine
  // config.cerevoice_eng.CPRCEN_engine_channel_speak(eng, chan_handle, "", 0, 1);
  // // Close the channel
  // config.cerevoice_eng.CPRCEN_engine_channel_close(eng, chan_handle);
  // // Delete the engine
  // config.cerevoice_eng.CPRCEN_engine_delete(eng);
  // return res;
}

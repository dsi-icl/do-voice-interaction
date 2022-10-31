// This file contains code to translate a textual input into audio
// output. This file will either use Cereproc TTS or Google TTS 
// depending on the settings in the tts_cereproc/config folder.
// The Cereproc method can be configured to either an in-memory
// buffer or a read-from-file method in the tts_cereproc/config folder.

import GTTS from 'gtts'
import { Base64Encode } from 'base64-stream'
import streamToPromise from 'stream-to-promise'
import fs from 'fs'
import wav from 'node-wav'
import cerevoiceEng from './cerevoice/sdk/cerevoice_eng/jslib/cerevoice_eng.node'
let buf = new Float32Array(0)
let eng;
let userData



export function setupEngine(){
  eng = cerevoiceEng.CPRCEN_engine_load(
    global.config.voice_file,
    global.config.licence_file,
    global.config.root_certificate,
    global.config.client_certificate,
    global.config.client_key
  );
  userData = new UserData(null, cerevoiceEng, eng, global.config)
}

 
class UserData {
  constructor(ws, crvc_eng, engine, config) {
      this.ws = ws
      this.crvc_eng = crvc_eng
      this.engine = engine
      this.config = config
  }
}


/**
 * Function that execute text to speech service get request
 * @param {Request} req The received request from the voice-assistant service
 * @param {Response} res The response to be sent to the voice-assistant service in stream format
 * @see {@link https://www.npmjs.com/package/gtts|Gtts}
 */
export async function textToSpeech (req, res) {
  try {
    if (global.config.cereprocOn) {
      cereSpeak(getParams(req), res)
      return
    } else {
      const data = await speak(getParams(req))
      res.status(200).json({ status: 'success', service: 'Text To Speech service', data, contentType: 'audio/wav' })
    }
  } catch (err) {
    res.status(400).json({ status: 'fail', service: 'Text To Speech service', error: err.toString() })
    console.log(err)
  }
}


function getParams (req) {
  return { text: req.query.text || req.body.text || '', lang: req.query.lang || req.body.lang || 'en-uk', thayers: req.body.thayers || 'n/a' }
}


function speak ({ text, lang }) {
  return streamToPromise(new GTTS(text, lang).stream().pipe(new Base64Encode())).then(data => data.toString())
}


function cereSpeak ({text, thayers}, res) {
  if (thayers!=="n/a"){
    let thayersArray=thayers.split(",").map(str=>Number(str))
    text = addMarkers(text, thayersArray)
  }
  if (global.config.cereFile){
    cereFile(text, res)
  }
  else {
    cereBuffer(text, res)
  }
}


function cereFile (text, res) {
  const file='./recordings/cerefile.wav'
  cerevoiceEng.CPRCEN_engine_speak_to_file(eng, text, file)
  const data = fs.readFileSync(file, { encoding: 'base64' })
  res.status(200).json({ status: 'success', service: 'Text To Speech service', data, contentType: 'audio/wav' })
  fs.unlinkSync(file)
}



function cereBuffer(text, res) {

  let chan_handle = cerevoiceEng.CPRCEN_engine_open_default_channel(eng);

  const resParameter = channel_callback.bind(null, res)

  cerevoiceEng.CPRCEN_engine_set_callback(eng, chan_handle, userData, resParameter);

  if (typeof text !== 'string'){
    res.status(400).send("Bad request");
    return 
  }

  cerevoiceEng.CPRCEN_engine_channel_speak(eng, chan_handle, text + "\n", text.length + 1, 1);
  cerevoiceEng.CPRCEN_engine_callback_delete()
  cerevoiceEng.CPRCEN_engine_channel_close(eng, chan_handle);
  return 
}

function channel_callback(res, abuf, userdata) {
  var cerevoice_eng = userdata.crvc_eng;

  // variable to check if the last spurt from the Cereproc Engine has arrived.
  // If so, dispatch the Res object. Otherwise, concatenate with buffer array.
  var final = false

  var trans_mk = cerevoice_eng.CPRC_abuf_trans_mk(abuf);
    var trans_done = cerevoice_eng.CPRC_abuf_trans_done(abuf);
    for (var i = trans_mk; i < trans_done; i++) {
        var trans = cerevoice_eng.CPRC_abuf_get_trans(abuf, i);
        var name = cerevoice_eng.CPRC_abuf_trans_name(trans);
        var type = cerevoice_eng.CPRC_abuf_trans_type(trans);
        if (type == cerevoice_eng.CPRC_ABUF_TRANS.CPRC_ABUF_TRANS_MARK) {
            if (name==="cprc_spurt_final"){
              final=true
            }
        }
    }



  var wav_added = cerevoice_eng.CPRC_abuf_added_wav_sz(abuf);
  var wav_mk = cerevoice_eng.CPRC_abuf_wav_mk(abuf);
  var f32a = new Float32Array(wav_added);
  for (var i = 0; i < wav_added; i++) {
      f32a[i] = cerevoice_eng.CPRC_abuf_wav(abuf, wav_mk + i) / 32768.0;
  } 

  buf=Float32Concat(buf, f32a)

  if (final){
    var sample_rate = cerevoice_eng.CPRC_abuf_wav_srate(abuf);

    buf = (new Array(1)).fill(buf)

    let buffer = wav.encode(buf, { sampleRate: sample_rate, float: true, bitDepth: 32 });

    var enc = new Uint8Array(buffer)
    var data = Buffer.from(enc).toString('base64')

    res.status(200).json({ status: 'success', service: 'Text To Speech service', data, contentType: 'audio/wav' })
    buf = new Float32Array(0)
  }
}



function Float32Concat(first, second)
{
    var firstLength = first.length,
        result = new Float32Array(firstLength + second.length);

    result.set(first);
    result.set(second, firstLength);

    return result;
}


function addMarkers(text, thayersArray){
  if (thayersArray[0]>0.5 && thayersArray[1]>0){
    return "<voice emotion='happy'> " + text + ", </voice>"
  }
  if (thayersArray[0]>0.5 && thayersArray[1]<0){
    return "<voice emotion='calm'>" + text + ", </voice>"
  }
  if (thayersArray[0]<-0.5 && thayersArray[1]<0){
    return "<voice emotion='sad'>" + text + ", </voice>"
  }
  if (thayersArray[0]<-0.5 && thayersArray[1]>0){
    return "<voice emotion='cross'>" + text + ", </voice>"
  }
  return text
}


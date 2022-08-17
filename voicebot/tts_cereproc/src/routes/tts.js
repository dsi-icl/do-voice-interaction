import GTTS from 'gtts'
import { Base64Encode } from 'base64-stream'
import streamToPromise from 'stream-to-promise'
import fs from 'fs'
import wav from 'node-wav'
import cerevoiceEng from './cerevoice/sdk/cerevoice_eng/jslib/cerevoice_eng.node'
let sectionCount;
let buf = new Float32Array(0)
let eng;
let userData



export function setupEngine(){
  // import('./cerevoice/sdk/cerevoice_eng/jslib/cerevoice_eng.node').then((cere)=>{
    // cerevoiceEng = cere;
  eng = cerevoiceEng.CPRCEN_engine_load(
    global.config.voice_file,
    global.config.licence_file,
    global.config.root_certificate,
    global.config.client_certificate,
    global.config.client_key
  );
  userData = new UserData(null, cerevoiceEng, eng, global.config)
// })
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

  let formattedText;

  ({sectionCount, formattedText} = countSections(text))

  cerevoiceEng.CPRCEN_engine_set_callback(eng, chan_handle, userData, resParameter);

  cerevoiceEng.CPRCEN_engine_channel_speak(eng, chan_handle, formattedText + "\n", formattedText.length + 1, 1);
  cerevoiceEng.CPRCEN_engine_callback_delete()
  cerevoiceEng.CPRCEN_engine_channel_close(eng, chan_handle);
  return 
}




function channel_callback(res, abuf, userdata) {

  var cerevoice_eng = userdata.crvc_eng;

  var wav_added = cerevoice_eng.CPRC_abuf_added_wav_sz(abuf);
  var wav_mk = cerevoice_eng.CPRC_abuf_wav_mk(abuf);
  var f32a = new Float32Array(wav_added);
  for (var i = 0; i < wav_added; i++) {
      f32a[i] = cerevoice_eng.CPRC_abuf_wav(abuf, wav_mk + i) / 32768.0;
  } 

  buf=Float32Concat(buf, f32a)
  sectionCount-=1

  if (sectionCount ===0){
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



function countSections(str = "") {
  let sectionCount = 0;
  str = str.replace(/[.,!?\n()"]/g, ",")
  str = str.replace(/(,)\1{1,}/g, ",")
  str=str.replace(/ '/g, ", ")
  str=str.replace(/\S,(\S)/g, ', $1')
  if (str.slice(-1)!==","&&str.slice(-1)!==">"){
    str+=","
  }
  for (const ch of str) {
    if (ch===",") {
      sectionCount++;
    }
    if (ch===">"){
      sectionCount+=0.5;
    }
  }
  return {"sectionCount": sectionCount, "formattedText": str};
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



// "<spurt audio='g0001_001'>c</spurt>"
// + "<spurt audio='g0001_002'>c</spurt>"
// + "<spurt audio='g0001_003'>c</spurt>"
// + "<spurt audio='g0001_004'>c</spurt>"
// + "<spurt audio='g0001_005'>c</spurt>"
// + "<spurt audio='g0001_006'>c</spurt>"
// + "<spurt audio='g0001_007'>c</spurt>"
// + "<spurt audio='g0001_008'>c</spurt>"
// + "<spurt audio='g0001_009'>c</spurt>"
// + "<spurt audio='g0001_010'>c</spurt>"
// + "<spurt audio='g0001_011'>c</spurt>"
// + "<spurt audio='g0001_012'>c</spurt>"
// + "<spurt audio='g0001_013'>c</spurt>"
// + "<spurt audio='g0001_014'>c</spurt>"
// + "<spurt audio='g0001_015'>c</spurt>"
// + "<spurt audio='g0001_016'>c</spurt>"
// + "<spurt audio='g0001_017'>c</spurt>"
// + "<spurt audio='g0001_018'>c</spurt>"
// + "<spurt audio='g0001_019'>c</spurt>"
// + "<spurt audio='g0001_020'>c</spurt>"
// + "<spurt audio='g0001_021'>c</spurt>"
// + "<spurt audio='g0001_022'>c</spurt>"
// + "<spurt audio='g0001_023'>c</spurt>"
// + "<spurt audio='g0001_024'>c</spurt>"
// + "<spurt audio='g0001_025'>c</spurt>"
// + "<spurt audio='g0001_026'>c</spurt>"
// + "<spurt audio='g0001_027'>c</spurt>"
// + "<spurt audio='g0001_028'>c</spurt>"
// + "<spurt audio='g0001_029'>c</spurt>"
// + "<spurt audio='g0001_030'>c</spurt>"
// + "<spurt audio='g0001_031'>c</spurt>"
// + "<spurt audio='g0001_032'>c</spurt>"
// + "<spurt audio='g0001_033'>c</spurt>"
// + "<spurt audio='g0001_034'>c</spurt>"
// + "<spurt audio='g0001_035'>c</spurt>"
// + "<spurt audio='g0001_036'>c</spurt>"
// + "<spurt audio='g0001_037'>c</spurt>"
// + "<spurt audio='g0001_038'>c</spurt>"
// + "<spurt audio='g0001_039'>c</spurt>"
// + "<spurt audio='g0001_040'>c</spurt>"
// + "<spurt audio='g0001_041'>c</spurt>"
// + "<spurt audio='g0001_042'>c</spurt>"
// + "<spurt audio='g0001_043'>c</spurt>"
// + "<spurt audio='g0001_044'>c</spurt>"
// + "<spurt audio='g0001_045'>c</spurt>"
// + "<spurt audio='g0001_046'>c</spurt>"
// + "<spurt audio='g0001_047'>c</spurt>"
// + "<spurt audio='g0001_048'>c</spurt>"
// + "<spurt audio='g0001_049'>c</spurt>"
// + "<spurt audio='g0001_050'>c</spurt>"
// + "<spurt audio='g0001_051'>c</spurt>"
// + "<spurt audio='g0001_052'>c</spurt>"
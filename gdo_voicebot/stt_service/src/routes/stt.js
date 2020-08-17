/**
 * @file Manages some deepspeech utilities functions
 * @author Aurélie Beaugeard
 */

/**
 * @import { isEmpty } from "./routes/index.js"
 * @see {@link "./routes/index.js"|index.js}
 */
import { isEmpty } from './index.js'

const DeepSpeech = require('deepspeech')

/**
 * Function that returns the transcription of an audioBuffer using deepspeech node.
 *
 * @param {Buffer} audioBuffer The audioBuffer to be transcripted (parameters to be verified : mono-channel,16000 Hz (sample rate), 16 bit PCM)
 * @param {DeepSpeech.Model} model The deepspeech model used to convert the speech to text
 * @returns {String} The text message from the user
 * @see {@link https://deepspeech.readthedocs.io/en/v0.7.4/NodeJS-API.html|DeepSpeech}
 */
function speechToText (audioBuffer, model) {
  return model.stt(audioBuffer)
}

/**
 * Function that returns a pre-constructed DeepSpeech Model object
 *
 * @description DEEPSPEECH VERSION: 0.7.4,
 * @description BEAM_WIDTH: 1024,
 * @description LM_ALPHA: 0.75,
 * @description LM_BETA: 1.85,
 * @see {@link https://deepspeech.readthedocs.io/en/v0.7.4/NodeJS-API.html|DeepSpeech}
 * @returns {DeepSpeech.Model} The model to be used for the transcription
 */
export function loadDeepSpeechModel () {
  const model = new DeepSpeech.Model(global.config.deepSpeechParameters.modelPath)
  model.setBeamWidth(global.config.deepSpeechParameters.BEAM_WIDTH)

  model.enableExternalScorer(global.config.deepSpeechParameters.scorerPath)
  model.setScorerAlphaBeta(global.config.deepSpeechParameters.LM_ALPHA, global.config.deepSpeechParameters.LM_BETA)

  return model
}

/**
 * Function that manages the post request from the stt service
 * @param {Request} req the received request from the voice-assistant service
 * @param {Response} res the response in json format
 * @param {DeepSpeech.Model} model the DeepSppech model to make the speech to text transcription
 */
export function executeSpeechToTextRequest (req, res, model) {
  // If we receive an empty buffer or an undefined object we send back an error to the voice assistant service.
  if (isEmpty(req.body)) {
    res.status(400).json({
      status: 'fail',
      service: 'Speech To Text service',
      message: 'The request body contains nothing'
    })
  } else {
    const buffer = Buffer.from(req.body, 'base64')
    const textMessage = speechToText(buffer, model)

    console.log('Text message :', textMessage)

    // If deepspeech transcription is empty we send back an error to the voice assistant service.
    if (textMessage.length === 0) {
      res.status(400).json({ status: 'fail', service: 'Speech To Text service', message: 'No transcription for this' })
    } else {
      // Everything is fine, we send back the textMessage
      res.status(200).json({ status: 'ok', service: 'Speech To Text service', text: textMessage })
    }
  }
}

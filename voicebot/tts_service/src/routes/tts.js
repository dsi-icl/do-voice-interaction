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
    const data = await speak(getParams(req))
    res.status(200).json({ status: 'success', service: 'Text To Speech service', data, contentType: 'audio/mpeg' })
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

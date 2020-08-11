/**
 * @file Manages some voice-assistant utilities functions
 * @author Aurélie Beaugeard
 */

import fetch from 'node-fetch'
import { mergeUrlParams } from '../util'

/**
 * This function returns a json response to be sent at the /api/json route.
 *
 * @param {Request} req The user's request
 * @param {Response} res The service response
 */
export function sampleData (req, res) {
  res.json({ data: 'sampleData' })
}

/**
 * This function returns the voice buffer sent by the Text To speech service thanks to a post request
 *
 * @param {URL} requestUrl The url to make the post request
 * @param {String} robotAnswer The robot text answer
 * @returns {ArrayBuffer} The voice answer encoded in an array buffer
 * @see {@link https://www.npmjs.com/package/node-fetch|Fetch}
 * @see {@link https://www.npmjs.com/package/gtts|Gtts}
 */
export async function getData (requestUrl, robotAnswer) {
  // We make the get request with the correct url (.../api/tts) and with the chosen parameters
  try {
    const response = await fetch(mergeUrlParams(requestUrl, { text: robotAnswer, lang: 'en' }))

    const status = await response.status
    if (status === 200) {
      return { success: true, data: new Buffer(response.arrayBuffer()).toString('base64') }
    } else if (status === 400) {
      return { success: false, ...response.json() }
    } else {
      return { success: false, ...response.json() }
    }
  } catch (exc) {
    return { success: false, text: exc.message }
  }
}

/**
 * This function is used to post the user's voice encoded in a blob to the speech to text service thanks to fetch.
 *
 * @param {URL} url The url to make the post request (.../api/stt)
 * @param {Blob} data The blob to be sent through the req body.
 * @param {String} serviceName The service concerned
 * @returns {JSON} The json response containing the status, the text transcription or the error message and the concerned service in case of error
 * @see {@link https://www.npmjs.com/package/node-fetch|Fetch}
 * @see {@link https://deepspeech.readthedocs.io/en/v0.7.4/NodeJS-API.html|DeepSpeech}
 */
export async function postData (url, data, serviceName) {
  let jsondata

  const response = await fetch(url, {
    method: 'post',
    // The content-type is important to be able to send the audio blob properly
    headers: { 'Content-type': 'text/plain' },
    body: data
  })
  try {
    jsondata = await response.json()
  } catch (error) {
    jsondata = {
      status: 'fail',
      service: serviceName,
      text: 'I encountered this error \'\'' + response.status + ' : ' + response.statusText + '\'\' in the ' + serviceName
    }
  }
  //todo; refactor this to be same as getData
  return jsondata
}

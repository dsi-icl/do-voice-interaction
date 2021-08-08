/**
 * @file Manages some voice-assistant utilities functions
 * @author Aurélie Beaugeard
 */

import fetch from 'node-fetch'
import { mergeUrlParams } from '../util'

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
    const response = await fetch(mergeUrlParams(requestUrl, { text: robotAnswer, lang: 'en-uk' }))

    const status = await response.status
    const data = await response.json()
    if (status >= 200 && status <= 299) {
      return { success: true, data: data.data, contentType: data.contentType }
    } else {
      return { success: false, text: data.error }
    }
  } catch (exc) {
    return { success: false, text: exc.message }
  }
}

/**
 * NEW getData more generic with only one parameter
 *
 * @param {URL} requestUrl The url to make the post request
 * @returns {ArrayBuffer} The voice answer encoded in an array buffer
 * @see {@link https://www.npmjs.com/package/node-fetch|Fetch}
 * @see {@link https://www.npmjs.com/package/gtts|Gtts}
 */
 export async function getDataRasa (requestUrl) {
  // We make the get request with the correct url (.../api/tts) and with the chosen parameters
    try {
      const response = await fetch(requestUrl, {
        method: 'get',
        // The content-type is important to be able to send the audio blob properly
        headers: { 'Content-type': 'text/plain' },
      })
      
      const status = response.status
      if (status >= 200 && status <= 299) {
        const data = await response.json()
        return { success: true, data: data, contentType: data.contentType }
      } else {
        return { success: false, text: data.error }
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
  try {
    const response = await fetch(url, {
      method: 'post',
      // The content-type is important to be able to send the audio blob properly
      headers: { 'Content-type': 'text/plain' },
      body: data
    })

    const status = await response.status
    const responseData = await response.json()

    if (status >= 200 && status <= 299) {
      return { success: true, data: responseData }
    } else {
      return { success: false, data: responseData }
    }
  } catch (exc) {
    return { success: false, data: { text: exc.message } }
  }
}

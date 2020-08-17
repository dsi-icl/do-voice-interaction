/**
 * @file Manages some voice-assistant utilities functions
 * @author Aurélie Beaugeard
 */

import { getData, postData } from './index.js'

/**
 * Function that manages the actions to do if the deepspeech transcription has been successfully done
 * @param {SocketIO.Client} client The client with which the server comunicates
 * @param {JSON} sttResponse The deepspeech json response
 */
export async function successProcess (client, sttResponse, request) {
  console.log('Speech to text transcription : SUCCESS\n')

  const botResult = await postData(global.config.services.doControlService, '{"message":"' + sttResponse.text + '"}', 'Data Observatory Control Service')

  console.log('bot result', botResult)

  let botResponseText = botResult.data
  let botResponseVoice = botResult.data

  if (botResult.success) {
    botResponseText = mergeText(botResult.data, ' ')
    botResponseVoice = mergeText(botResult.data, ', ')
  }

  // We send the text message to the tts service to get back the voice answer.
  const voiceAnswer = await getData(global.config.services.ttsService, botResponseVoice)
  console.log('Voice answer (success) : ', voiceAnswer)

  if (voiceAnswer.success) {
    // The user receives a transcript of her or his voice message for verification.
    // The text version of the bot answer is also sent and displayed on the user interface
    // Voice answer sent to the client through the socket
    client.emit('response', {
      id: request.id,
      date: request.date,
      command: sttResponse.text,
      response: botResponseText,
      audio: {
        data: voiceAnswer.data
      }
    })
  } else {
    // If Gtts raised an error, we send it to the client
    await errorProcess(client, voiceAnswer, sttResponse.data, request)
  }
}

/**
 * Function that manages the actions to do if one of the service failed
 * @param {SocketIO.Client} client The client with which the server comunicates
 * @param {JSON} errorResponse The error json response
 * @param {String} sttResponseText The text received from the Speech To Text service
 */
export async function errorProcess (client, errorResponse, sttResponseText, request) {
  // We generate an error voice message
  const voiceAnswer = await getData(global.config.services.ttsService, 'I encountered an error. Please consult technical support or try the request again')

  console.log('Voice answer (fail)', voiceAnswer)

  // We send the json content response to the client, to give a description to the user in an alert box
  // The voice alert is sent to the client to be played
  client.emit('response', {
    id: request.id,
    date: request.date,
    command: sttResponseText !== '' ? sttResponseText : '...',
    audio: {
      data: voiceAnswer.success ? voiceAnswer.data : null
    },
    error: errorResponse.text
  })
}

export async function processAudioCommand (client, request) {
  if (request.audio.type !== 'audio/wav' || request.audio.sampleRate !== 16000) {
    const error = { status: 'fail', service: 'Voice-assistant service', text: 'The record format is wrong' }
    await errorProcess(client, error, '', request)
  } else {
    // We get the audio blob and send it to the stt service
    const audioData = request.audio.data.split(',').pop()

    const sttResponse = await postData(global.config.services.sttService, audioData, 'Speech To Text Service')

    console.log('sttresponse', sttResponse)

    // If an error was encountered during the request or the string response is empty we inform the user through the event problem with the socket.
    // Else we can send the text transcript to the the text to speech service and sending the audiobuffer received to the client.
    if (sttResponse.success) {
      await successProcess(client, sttResponse.data, request)
    } else {
      await errorProcess(client, sttResponse.data, '', request)
    }
  }
}

export async function processTextCommand (client, request) {
  const commandData = { data: request.command }

  if (commandData.data === '') {
    const error = { status: 'fail', service: 'Voice-assistant service', text: 'Nothing has been written' }
    await errorProcess(client, error, '', request)
  } else {
    await successProcess(client, commandData, request)
  }
}

/**
 * Function used to merge a text answer
 * @param {JSON} result The json response
 * @param {String} separator the separator to use
 * @returns {String} The text answer
 */
function mergeText (result, separator) {
  if (Array.isArray(result)) {
    return result.map(e => e.text).join(separator)
  } else {
    return Object.property.hasOwnProperty.call(result, 'text') ? result.text : ''
  }
}

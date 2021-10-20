/**
 * @file Manages some voice-assistant utilities functions
 * @author Aurélie Beaugeard
 */

import { getData, getDataRasa, postData } from './index.js'

/**
 * Function that manages the actions to do if the deepspeech transcription has been successfully done
 * @param {SocketIO.Client} client The client with which the server comunicates
 * @param {JSON} sttResponse The deepspeech json response
 */
export async function successProcess (client, sttResponse, request, recentEmotion, errorCorrectionMessage) {
  // TODO: take care of errorCorrectionMessage
  console.log('Speech to text transcription : SUCCESS\n')

  const botResult = await postData(global.config.services.dialogManagerService, '{"message":"' + sttResponse.text + '"}', 'Data Observatory Control Service')

  console.log('bot result', botResult)

  if (botResult.success) {
    const botResponseText = mergeText(botResult.data, '\n')
    const botResponseVoice = mergeText(botResult.data, ', ')

    // We send the text message to the tts service to get back the voice answer.
    const voiceAnswer = await getData(global.config.services.ttsService, botResponseVoice)

    if (voiceAnswer.success) {
      // The user receives a transcript of her or his voice message for verification.
      // The text version of the bot answer is also sent and displayed on the user interface
      // Voice answer sent to the client through the socket
      client.emit('response', {
        id: request.id,
        date: request.date,
        command: sttResponse.text,
        emotion: recentEmotion,
        response: botResponseText,
        audio: {
          data: voiceAnswer.data,
          contentType: voiceAnswer.contentType
        }
      })
    } else {
      // If Gtts raised an error, we send it to the client
      await errorProcess(client, voiceAnswer, sttResponse.text, request)
    }
  } else {
    await errorProcess(client, botResult.data, sttResponse.text, request)
  }
}

/**
 * Function that manages the actions to do if one of the service failed
 * @param {SocketIO.Client} client The client with which the server comunicates
 * @param {JSON} errorResponse The error json response
 * @param {String} sttResponseText The text received from the Speech To Text service
 */
export async function errorProcess (client, errorResponse, sttResponseText, request, recentEmotion = 'error') {
  // We generate an error voice message
  const voiceAnswer = await getData(global.config.services.ttsService, 'I encountered an error. Please consult technical support or try the request again')

  // We send the json content response to the client, to give a description to the user in an alert box
  // The voice alert is sent to the client to be played
  client.emit('response', {
    id: request.id,
    date: request.date,
    command: sttResponseText !== '' ? sttResponseText : '...',
    emotion: recentEmotion,
    audio: {
      data: voiceAnswer.data,
      contentType: voiceAnswer.contentType
    },
    error: errorResponse.text
  })
}

export async function processErrorCorrection (sttResponse) {
  const dataForErrorCorrection = { transcript: sttResponse.text }
  const errorCorrectionResponse = await postData(global.config.services.errorCorrectionService, JSON.stringify(dataForErrorCorrection), 'Error Correction Service')
  console.log('errorCorrectionResponse ', errorCorrectionResponse)

  if (errorCorrectionResponse.success) {
    return [errorCorrectionResponse, null]
  } else {
    return [errorCorrectionResponse, 'error']
  }
}

export async function processEmotion (speech, sttResponse) {
  var emotion = 'n/a'
  const dataForEmotionRecognition = { audio: speech, transcript: sttResponse.text }
  const emotionRecognitionResponse = await postData(global.config.services.emotionRecognitionService, JSON.stringify(dataForEmotionRecognition), 'Emotion Recognition Service')
  console.log('emotionRecognitionResponse ', emotionRecognitionResponse)

  if (emotionRecognitionResponse.success) {
    emotion = emotionRecognitionResponse.data.emotion

    // Set the emotion slot in rasa via http api
    const newData = { event: 'slot', timestamp: null, name: 'emotion', value: emotion }
    const botResult = await postData(global.config.services.rasaTrackerEvents, JSON.stringify(newData), 'Data Observatory Control Service')
    console.log('set emotion in rasa ', botResult)

    return [emotion, null]
  } else {
    return [emotion, emotionRecognitionResponse.data]
  }
}

export async function processAudioCommand (client, request) {
  if (request.audio.type !== 'audio/wav' || request.audio.sampleRate !== 16000) {
    const error = { status: 'fail', service: 'Voice-assistant service', text: 'The record format is wrong' }
    await errorProcess(client, error, '', request)
  } else {
    const sttResponse = await postData(global.config.services.sttService, request.audio.data, 'Speech To Text Service')
    console.log('sttresponse', sttResponse)

    // If an error was encountered during the request or the string response is empty we inform the user through the event problem with the socket.
    // Else we can send the text transcript to the the text to speech service and sending the audiobuffer received to the client.
    if (sttResponse.success) {
      // Get tracker information from rasa
      const tracker = await getDataRasa(global.config.services.rasaTracker)
      // Get rasa's slot values
      const slots = tracker.data.slots
      // Only carry out emotion recognition if the speaker currently has it enabled in the slot
      var emotion = 'n/a'
      var errorCorrectionMessage = 'n/a'
      var error
      if (slots.emotion_detection_enabled) {
        [emotion, error] = await processEmotion(request.audio.data, sttResponse.data)
        // TODO: look into what processEmotion failure means and if we want to fail here or continue
        if (error != null) {
          await errorProcess(client, error, '', request)
          return
        }
      }

      if (slots.error_correction_enabled) {
        // Only carry out error correction if the speaker currently has it enabled in the slot
        [errorCorrectionMessage, error] = await processErrorCorrection(sttResponse.data)
        if (error != null) {
          await errorProcess(client, error, '', request)
          return
        }
      }

      await successProcess(client, sttResponse, request, emotion, errorCorrectionMessage)
    } else {
      await errorProcess(client, sttResponse.data, '', request)
    }
  }
}

export async function processTextCommand (client, request) {
  const commandData = { text: request.command }

  if (commandData.data === '') {
    const error = { status: 'fail', service: 'Voice-assistant service', text: 'Nothing has been written' }
    await errorProcess(client, error, '', request)
  } else {
    // Get tracker information from rasa
    const tracker = await getDataRasa(global.config.services.rasaTracker)
    // Get rasa's slot values
    const slots = tracker.data.slots
    var errorCorrectionMessage = 'n/a'
    var error
    if (slots.error_correction_enabled) {
      // Only carry out error correction if the speaker currently has it enabled in the slot
      [errorCorrectionMessage, error] = await processErrorCorrection(request.command)
      if (error != null) {
        await errorProcess(client, error, '', request)
        return
      }
    }

    await successProcess(client, commandData, request, 'no detection for text-only command.', errorCorrectionMessage)
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

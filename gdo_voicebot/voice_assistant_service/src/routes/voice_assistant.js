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
export async function successProcess (client, sttResponse) {
  console.log('Speech to text transcription : SUCCESS\n')

  var botResult = await postData(global.config.services.doControlService, '{"message":"' + sttResponse.text + '"}',"Data Observatory Control Service")
  var botResponseText = prepareBotTextAnswer(botResult)
  var botResponseVoice = prepareBotVoiceAnswer(botResult)

  // We send the text message to the tts service to get back the voice answer.
  const voiceAnswer = await getData(global.config.services.ttsService, botResponseVoice)

  if (voiceAnswer instanceof ArrayBuffer) {
    // The user receives a transcript of her or his voice message for verification.
    client.emit('user-request', { user: sttResponse.text })
    // The text version of the bot answer is also sent and displayed on the user interface
    client.emit('robot-answer', { robot: botResponseText })
    // Voice answer sent to the client through the socket
    client.emit('result', voiceAnswer)
  } else {
    // If Gtts raised an error, we send it to the client
    errorProcess(client, voiceAnswer,sttResponse.text)
  }
}

/**
 * Function that manages the actions to do if one of the service failed
 * @param {SocketIO.Client} client The client with which the server comunicates
 * @param {JSON} errorResponse The error json response
 * @param {String} sttResponseText The text received from the Speech To Text service
 */
export async function errorProcess (client, errorResponse,sttResponseText) {
  // We geerate an error voice message
  const voiceAnswer = await getData(global.config.services.ttsService, 'I encountered an error. Please consult technical support or try the request again')

  // We send the json content response to the client, to give a description to the user in an alert box
  client.emit('problem', errorResponse)

  // The voice alert is sent to the client to be played
  client.emit('voice-alert', voiceAnswer)

  if(sttResponseText!==""){
    client.emit('user-request', { user: sttResponseText })
  } else {
    // We indicate to the user that its message is not perceived.
    client.emit('user-request', { user: '...' })
  }


  // Console error messages
  console.log('Status :', errorResponse.status)
  console.log('Concerned service : ', errorResponse.service)
  console.log('Error message :', errorResponse.message + '\n')
}

/**
 * Function that manage the entire communication process between the server and the client
 * @param {SocketIO.Client} client The client with which the server comunicates
 */
export function echoProcess (client) {
  console.log('Client connected\n')

  // The user has recorded a message and the client sent it to the server
  client.on('message', async function (data) {
    console.log('RECORD DONE\n')

    // We get the audio blob and send it to the stt service
    const dataURL = data.audio.dataURL.split(',').pop()

    const sttResponse = await postData(global.config.services.sttService, dataURL,"Speech To Text Service")

    // If an error was encountered during the request or the string response is empty we inform the user through the event problem with the socket.
    // Else we can send the text transcript to the the text to speech service and sending the audiobuffer received to the client.
    if (sttResponse.status === 'ok') {
      successProcess(client, sttResponse)
    } else {
      errorProcess(client, sttResponse, "")
    }
  })
}

/**
 * Function used to shape the bot text answer displayed on the UI
 * @param {JSON} botResult The json response from the chatbot
 * @returns {String} The bot text answer
 */
function prepareBotTextAnswer (botResult) {
  var result = ''
  botResult.forEach(element => {
    result += element.text + '</br>'
  })
  return result
}

/**
 * Function used to shape the bot text answer sent to the tts service. All has to be in one line to get an entire voice response from gtts
 * @param {JSON} botResult The json response from the chatbot
 * @returns {String} The bot text answer sent to the tts service
 */
function prepareBotVoiceAnswer (botResult) {
  var result = ''
  botResult.forEach(element => {
    result += element.text + ', '
  })
  return result
}

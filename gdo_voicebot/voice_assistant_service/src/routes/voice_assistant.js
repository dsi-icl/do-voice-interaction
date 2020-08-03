import { getData, postData } from './index.js'

export async function successProcess (client, sttResponse) {
  console.log('Speech to text transcription : SUCCESS\n')

  // The user receives a transcript of her or his voice message for verification.
  client.emit('user-request', { user: sttResponse.text })

  // We send the text message to the tts service to get back the voice answer.
  const voiceAnswer = await getData(global.config.tts_service, 'The Data Observatory control service has not been integrated yet')

  // Voice answer sent to the client through the socket
  client.emit('result', voiceAnswer)

  // The text version of the bot answer is also sent and displayed on the user interface
  client.emit('robot-answer', { robot: 'The DO control service has not been integrated yet' })
}

export async function errorProcess (client, sttResponse) {
  // We geerate an error voice message
  const voiceAnswer = await getData(global.config.tts_service, 'I encountered an error. Please consult technical support or try the request again')

  // We send the json content response to the client, to give a description to the user in an alert box
  client.emit('problem', sttResponse)

  // The voice alert is sent to the client to be played
  client.emit('voice-alert', voiceAnswer)

  // We indicate to the user that its message is not perceived.
  client.emit('user-request', { user: '...' })

  // Console error messages
  console.log('Speech to text transcription : FAIL\n')
  console.log('Status :', sttResponse.status)
  console.log('Concerned service : ', sttResponse.service)
  console.log('Error message :', sttResponse.message + '\n')
}

export function echoProcess (client) {
  console.log('Client connected\n')

  // The user has recorded a message and the client sent it to the server
  client.on('message', async function (data) {
    console.log('RECORD DONE\n')

    // We get the audio blob and send it to the stt service
    const dataURL = data.audio.dataURL.split(',').pop()

    const sttResponse = await postData(global.config.stt_service, dataURL)

    // If an error was encountered during the request or the string response is empty we inform the user through the event problem with the socket.
    // Else we can send the text transcript to the the text to speech service and sending the audiobuffer received to the client.
    if (sttResponse != null && sttResponse.status === 'ok') {
      successProcess(client, sttResponse)
    } else {
      errorProcess(client, sttResponse)
    }
  })
}

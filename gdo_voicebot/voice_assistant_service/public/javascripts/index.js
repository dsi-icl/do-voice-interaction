/**
 * @file Manages utils functions used by the client
 * @author Aurélie Beaugeard
*/

var hark = require('../hark.js')
var RecordRTC = require('recordrtc')

/**
 * Function that instanciated and return a hark object
 *
 * @param {Stream} stream The navigator stream
 * @param {Options} options The options that can be added : interval, threshold, play, audioContext
 * @returns {Hark} The hark object
 * @see{@link https://www.npmjs.com/package/hark|hark}
 * @see{@link https://github.com/otalk/hark|Hark}
 */
function Hark (stream, options) {
  return hark(stream, options)
}

/**
 * Function that instanciates the recorder
 * @param {Stream} stream the stream from the navigator
 * @see{@link https://www.npmjs.com/package/recordrtc|recordrtc}
 * @see{@link https://github.com/muaz-khan/RecordRTC|RecordRTC}
 */
function initRecorder (stream) {
  // An error is raised if we couldn't create the RecordRTC object properly
  // RecordRTC options must be adapted according to the used Speech-To-Text tool (default :DeepSpeech)
  try {
    recorder = RecordRTC(stream, {
      recorderType: StereoAudioRecorder,
      type: 'audio',
      mimeType: 'audio/wav',
      numberOfAudioChannels: 1,
      desiredSampRate: 16000
    })
  } catch (err) {
    alert(err.name)
  }
}

/**
 * Function that reset buttons state (initial states)
 * @param {HTMLButtonElement} recordButton The recordbutton would be enabled
 * @param {HTMLButtonElement} stopButton The stopButton would be disabled
 */
function resetButtonsState (recordButton, stopButton) {
  recordButton.disabled = false
  stopButton.disabled = true
}

/**
 * Functions that checks if the navigator support WebRTC getUserMedia and if it supports only deprecated getUserMedia API
 * @param {window.navigator} navigator The user's navigator
 */
function checkNavigator (navigator) {
  if (typeof navigator.mediaDevices === 'undefined' || !navigator.mediaDevices.getUserMedia) {
    alert('This browser does not supports WebRTC getUserMedia API.')

    if (navigator.getUserMedia) {
      alert('This browser seems supporting deprecated getUserMedia API.')
    }
  }
}

/**
 * Function that changes buttons state to record states
 * @param {HTMLButtonElement} recordButton The recordButton would be disabled
 * @param {HTMLButtonElement} stopButton The stopButton would be enabled
 */
function buttonsStateRecord (recordButton, stopButton) {
  // Buttons state update
  recordButton.disabled = true
  stopButton.disabled = false
}

/**
 * Function that plays the gtts audio voice message
 * @param {ArrayBuffer} audioData The audio buffer received from the voice-assistant server
 * @param {AudioContext} audioContext The client AudioContext
 * @param {AudioBufferSourceNode} source The client AudioBufferSourceNode
 * @param {String} dataBot The bot answer
 * @param {HTMLUListElement} listMessages The list that contains the conversation
 * @param {HTMLButtonElement} recordButton The record button to be enabled
 * @param {HTMLButtonElement} stopButton The stop button to be disabled
 * @see{@link https://developer.mozilla.org/fr/docs/Web/API/AudioContext|AudioContext}
 */
function play (audioData, audioContext, source, dataRobot, listMessages, recordButton, stopButton) {
  source = audioContext.createBufferSource()
  audioContext.decodeAudioData(audioData, function (buffer) {
    source.buffer = buffer
    source.connect(audioContext.destination)
    source.start(0)
    source.onended = function() {
      updateListMessages(dataRobot,listMessages)
      resetButtonsState(recordButton,stopButton)
    }
    return source
  },
  function (e) { console.log('Error with decoding audio data' + e.err) })
};

/**
 * Function that plays the gtts audio voice message
 * @param {ArrayBuffer} audioData The audio buffer received from the voice-assistant server
 * @param {AudioContext} audioContext The client AudioContext
 * @param {AudioBufferSourceNode} source The client AudioBufferSourceNode
 * @param {Dictionnary} errorData The error details
 * @param {HTMLUListElement} listMessages The list that contains the conversation
 * @param {HTMLButtonElement} recordButton The record button to be enabled
 * @param {HTMLButtonElement} stopButton The stop button to be disabled
 * @see{@link https://developer.mozilla.org/fr/docs/Web/API/AudioContext|AudioContext}
 */
function playError (audioData, audioContext, source, errorData, listMessages, recordButton, stopButton) {
  source = audioContext.createBufferSource()
  audioContext.decodeAudioData(audioData, function (buffer) {
    source.buffer = buffer
    source.connect(audioContext.destination)
    source.start(0)
    source.onended = function() {
      displayErrorMessage(errorData,listMessages)
      resetButtonsState(recordButton,stopButton)
    }
    return source
  },
  function (e) { console.log('Error with decoding audio data' + e.err) })
};

/**
 * Function that stop the record and send it to the voice-assistant server
 * @param {HTMLSpanElement} message The message to be displayed on the user interface
 * @param {RecordRTC} recorder The recorder to be stopped
 * @param {Stream} mediaStream The mediaStrem to be stopped
 * @param {Socketio} socket The socket to use to emit the record
 */
function sendRecord (message, recorder, mediaStream, socket) {
  // Indicate the end of speech detection to the user
  message.innerHTML = "<font color='green'>You stopped talking. Your message will be sent to the server</font>"

  // We stop the recorder
  recorder.stopRecording(function () {
    recorder.getDataURL(function (audioDataURL) {
      var files = {
        audio: {
          type: recorder.getBlob().type || 'audio/wav',
          dataURL: audioDataURL
        }
      }

      // We send the audioData blob to the server which will be used for the Speech to Text transcription
      socket.emit('message', files)

      // Stop the stream...
      if (mediaStream) mediaStream.stop()
    })
  })
  recorder.clearRecordedData()
}

/**
 * Function that updates the conversation
 * @param {String} textMessage The message to be displayed on the user interface
 * @param {HTMLUListElement} listMessages The list that contains the conversation
 */
function updateListMessages(textMessage, listMessages){
  var message = document.createElement('li');
  message.innerHTML = "BOT ANSWER : " + textMessage
  listMessages.appendChild(message)
}

/**
 * Function that displays the error message
 * @param {String} textMessage The message to be displayed on the user interface
 * @param {HTMLUListElement} listMessages The list that contains the conversation
 */
function displayErrorMessage(textMessage, listMessages){
  var message = document.createElement('li')
  message.innerHTML = "BOT ANSWER : I encountered this error ''" + textMessage["message"] + "'' in the " + textMessage["service"] + ". Request status : " + textMessage["status"] + "."
  listMessages.appendChild(message)
}

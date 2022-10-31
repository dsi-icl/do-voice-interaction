/////// This file contains code to test the Rasa Dialogue Manager Service running locally. 
/////// Emotion detection must be activated to receive emotionally conditioned responses.

const fetch = require('node-fetch');

// This function is copied from the voice_assistant_service

async function postDataRasa (url, data, serviceName) {
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

// uncomment commands below to test bot's reponse to different prompts

let commandForDialogManager = "Because I don't want others to gossip about me"
// let commandForDialogManager = "Or! Or, we could go to the bank, close our accounts and cut them off at the source."
// let commandForDialogManager = "good morning"
let dialogManagerService="http://localhost:5005/webhooks/rest/webhook"

let botThayers="-0.8,0.9"

async function test (){
    const botResult = await postDataRasa(dialogManagerService, '{"message":"' + commandForDialogManager + '","emotion":"' + botThayers + '"}', 'Data Observatory Control Service')
    console.log(botResult)
}
test()
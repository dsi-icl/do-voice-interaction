const fetch = require('node-fetch');


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


// let commandForDialogManager = "turn on emotion recognition"
// let commandForDialogManager = "lets have a chat"
// let commandForDialogManager = "yes"
let dialogManagerService="http://localhost:5005/webhooks/rest/webhook"

let botThayers="0.4,0.5"//"n/a"

async function dod (){
    const botResult = await postDataRasa(dialogManagerService, '{"message":"' + commandForDialogManager + '","emotion":"' + botThayers + '"}', 'Data Observatory Control Service')
    console.log(botResult)
}
dod()
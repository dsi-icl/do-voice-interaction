// This file contains code to test the tts_cereproc service
// running locally. It makes the request using node-fetch.

const fs = require('fs')
const fetch = require('node-fetch')


const robotAnswer=[
    {
      recipient_id: 'default',
      text: "n/a",
   }
  ]

x= [
  {
    recipient_id: 'default',
    text: "I don't know, Chandler is supposed to be passin' ‘em around...",
  }
]

  function mergeText (result, separator) {
    if (Array.isArray(result)) {
      let x = result.map(e => e.text)
      let y = x.join(separator)
      console.log(x)
      console.log(y)
      return y
    } else {
      return Object.property.hasOwnProperty.call(result, 'text') ? result.text : ''
    }
  }

  botResult ={
       success: true,
       data: [
         {
           recipient_id: 'default',
           text: 'No worries',
           bot_thayers: '-0.559, 0.639'
         }
       ]
     }
  
botThayers=botResult.data[0].bot_thayers

console.log(JSON.stringify({text: mergeText(x, ', '), thayers: botThayers}))

async function run(){
  const response = await fetch('http://localhost:5000/api/tts', {
      method: 'post',
      headers: { 'Content-type': 'application/json' },
      body: JSON.stringify({text: mergeText(x, ', '), thayers: botThayers})
    })
    const status =  response.status
    const res = await response.json()
    const wavUrl = `data:audio/wav;base64,${res.data}`
    const buffer = Buffer.from(
    wavUrl.split('base64,')[1],  'base64')
    fs.writeFileSync('./response.wav', buffer)
    console.log(`wrote ${buffer.byteLength.toLocaleString()} bytes to file.`)
  }


run()




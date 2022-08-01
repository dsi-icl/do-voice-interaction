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
    text: "I'm sorry, something went wrong. I can't access to any demo if no environment is open. Please, open one of these environments before : students"
  },
  { recipient_id: 'default', text: 'Do you want me to try again ?' }
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

async function run(){
  const response = await fetch('http://localhost:5000/api/tts', {
      method: 'post',
      headers: { 'Content-type': 'application/json' },
      body: JSON.stringify({text: mergeText(x, ', '), thayers: "[0.61 , -0.85]"})
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




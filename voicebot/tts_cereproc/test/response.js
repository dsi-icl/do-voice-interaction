import fs from 'fs'
import fetch from 'node-fetch'


const robotAnswer=[
    {
      recipient_id: 'default',
      text: "I could be saying this with any emotion, It is up to you to decide what that is.",
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


const response =  await fetch('http://localhost:5000/api/tts', {
    method: 'post',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({text: mergeText(robotAnswer, ', '), thayers: "[0.61 , -0.85]"})
  })
  const status =  response.status
  const res = await response.json()
  const wavUrl = `data:audio/wav;base64,${res.data}`
  const buffer = Buffer.from(
  wavUrl.split('base64,')[1],  'base64')
  fs.writeFileSync('./response.wav', buffer)
  console.log(`wrote ${buffer.byteLength.toLocaleString()} bytes to file.`)



    




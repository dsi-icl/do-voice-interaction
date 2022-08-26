
const axios = require('axios');
const fs = require('fs')


axios
//   .post('http://do-voice-tts-cereproc:5000/api/tts', {
    .post('http://localhost:5000/api/tts', {
        text:"I don't know, Chandler is supposed to be passin' ‘em around...",thayers:"-0.459, 0.539"
})
  .then(res => {
    console.log(`statusCode: ${res.status}`);
    console.log(res);
    const wavUrl = `data:audio/wav;base64,${res.data.data}`
    const buffer = Buffer.from(
      wavUrl.split('base64,')[1],  'base64')
      fs.writeFileSync('./response.wav', buffer)
      console.log(`wrote ${buffer.byteLength.toLocaleString()} bytes to file.`)
  })
  .catch(error => {
    console.error(error);
  });


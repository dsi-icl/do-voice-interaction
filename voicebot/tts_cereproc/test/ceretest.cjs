
const axios = require('axios');

axios
//   .post('http://do-voice-tts-cereproc:5000/api/tts', {
    .post('http://localhost:5000/api/tts', {
        text:"I don't know, Chandler is supposed to be passin' ‘em around...",thayers:"-0.559, 0.639"
})
  .then(res => {
    console.log(`statusCode: ${res.status}`);
    console.log(res);
  })
  .catch(error => {
    console.error(error);
  });

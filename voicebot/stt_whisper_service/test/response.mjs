import fetch from 'node-fetch'

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

const base64_encoding = "Encoding goes here"

async function testResponse(){
    const sttResponse = await postDataRasa("http://localhost:3000/api/stt", base64_encoding, 'Speech To Text Service')
    console.log(sttResponse)
}

testResponse()
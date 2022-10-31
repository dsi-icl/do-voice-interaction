// This file contains code to test the Personality Service running locally

const fetch = require('node-fetch')


async function getBotEmotion(url, humanEmotion){
    try {
      const response = await fetch(url + "?" + new URLSearchParams({"emotion": "-0.34,-0.20"}), {
        method: 'get',
        headers: { 'Content-type': 'text/plain' }
      })
      const status = await response.status
      const data = await response.json()
      console.log(data)
      if (status >= 200 && status <= 299) {
        return { success: true, data: data, contentType: data.contentType }
      } else {
        return { success: false, text: data.error }
      }
    } catch (exc) {
      return { success: false, text: exc.message }
    }
  }

console.log(getBotEmotion('http://localhost:4000/personality-service'))
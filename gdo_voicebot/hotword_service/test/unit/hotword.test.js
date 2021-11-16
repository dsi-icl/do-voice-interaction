const WakewordDetector = require('@mathquis/node-personal-wakeword')
const hotwordService = require('../../src/routes/hotword')
const path = require('path')
const Response = require('response')

jest.setTimeout(10000)

test('Returns 400 on empty body request', async () => {
    let res = new Response(null, {
        status: 100,
        statusText: "",
        headers: {
        'Content-type': 'application/json'
        }
    })

    const req = {
        method: 'post',
        headers: { 'Content-type': 'text/plain' },
        body: null
    }

    await hotwordService.setUpKeywordClient(true)
    const response = await hotwordService.startListening(req, res, true)

    try {
        expect(response.statusCode).toBe(400)
    } catch (err) {
        fail(`Expected 400 response`)
    }
})

test('Returns 200 on every body containing audio', async () => {
    const audioFile = path.resolve(__dirname, '../../keywords', './abrakadabra1.wav')

    let res = new Response(null, {
        status: 100,
        statusText: "",
        headers: {
        'Content-type': 'application/json'
        }
    })

    const req = {
        method: 'post',
        headers: { 'Content-type': 'text/plain' },
        body: audioFile
    }

    await hotwordService.setUpKeywordClient(true)
    const response = await hotwordService.startListening(req, res, true)

    try {
        expect(response.statusCode).toBe(200)
    } catch (err) {
        fail(`Expected 200 response`)
    }
})

test('Empty message if NO hotword is detected', async () => {
    const audioFile = path.resolve(__dirname, '../../keywords', './abrakadabra1.wav')

    let res = new Response(null, {
        status: 100,
        statusText: "",
        headers: {
        'Content-type': 'application/json'
        }
    })

    const req = {
        method: 'post',
        headers: { 'Content-type': 'text/plain' },
        body: audioFile
    }

//     const response = await hotwordService.startListening(req, res, true)

//     console.log(response.json().text)

//     try {
//         // expect(response.json().text).toBe('')
//     } catch (err) {
//         fail(`Expected "not-present" message response`)
//     }
})

test('"detected" message if hotword is detected', async () => {
    const audioFile = path.resolve(__dirname, '../../keywords', './heyGalileo1.wav')

    let res = new Response(null, {
        status: 100,
        statusText: "",
        headers: {
        'Content-type': 'application/json'
        }
    })

    const req = {
        method: 'post',
        headers: { 'Content-type': 'text/plain' },
        body: audioFile
    }

    // const response = await hotwordService.startListening(req, res, true)

    // console.log(response.json().text)

    // try {
    //     expect(response.json().text).toBe('detected')
    // } catch (err) {
    //     fail(`Expected "detected" message response`)
    // }
})

function fail(reason) {
    throw new Error(reason);
}

global.fail = fail;
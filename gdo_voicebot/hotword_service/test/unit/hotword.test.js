const hotwordService = require('../../src/routes/hotword')
const path = require('path')
const Response = require('response')

jest.setTimeout(30000)

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

    // hotwordService.setUpKeywordClient(true)
    const response = await hotwordService.startListening(req, res, true)

    try {
        expect(response.statusCode).toBe(400)
    } catch (err) {
        fail(`Expected 400 response`)
    }
})

describe('Sending hotword audio to service ', () => {
    let res
    let req

    beforeAll(() => {
        const audioFile = path.resolve(__dirname, '../../keywords', './heyGalileo2.wav')

        res = new Response(null, {
            status: 100,
            statusText: "",
            headers: {
            'Content-type': 'application/json'
            }
        })

        req = {
            method: 'post',
            headers: { 'Content-type': 'text/plain' },
            body: audioFile
        }

    })

    it('should give response', (done) => {
        hotwordService.startListening(req, res, true, doneDetected = done, doneRandom = () => {})
    })
})

describe('Sending random audio to service ', () => {
    let res
    let req

    beforeAll(() => {
        const audioFile = path.resolve(__dirname, '../../keywords', './abrakadabra1.wav')

        res = new Response(null, {
            status: 100,
            statusText: "",
            headers: {
            'Content-type': 'application/json'
            }
        })

        req = {
            method: 'post',
            headers: { 'Content-type': 'text/plain' },
            body: audioFile
        }

    })

    it('should not detect anything', (done) => {
        hotwordService.startListening(req, res, true, doneDetected = () => {}, doneRandom = done)
    })
})

describe('Sending multiple requests ', () => {
    let res
    let req1
    let req2

    beforeAll(() => {
        const audioFile1 = path.resolve(__dirname, '../../keywords', './heyGalileo2.wav')
        const audioFile2 = path.resolve(__dirname, '../../keywords', './abrakadabra1.wav')

        res = new Response(null, {
            status: 100,
            statusText: "",
            headers: {
            'Content-type': 'application/json'
            }
        })

        req1 = {
            method: 'post',
            headers: { 'Content-type': 'text/plain' },
            body: audioFile1
        }

        req2 = {
            method: 'post',
            headers: { 'Content-type': 'text/plain' },
            body: audioFile2
        }

    })

    it('should not destroy detector', (done) => {
        hotwordService.startListening(req1, res, true, doneDetected = done, doneRandom = () => {})
        hotwordService.startListening(req2, res, true, doneDetected = () => {}, doneRandom = done)
        hotwordService.startListening(req1, res, true, doneDetected = done, doneRandom = () => {})
    })
})

function fail(reason) {
    throw new Error(reason)
}

global.fail = fail
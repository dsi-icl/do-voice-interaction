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

    hotwordService.setUpKeywordClient(true)
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

function fail(reason) {
    throw new Error(reason);
}

global.fail = fail;

// test('My test ', (done) => {
// 	let detected = false
// 	main(done, detected)
// })

// async function main(done, detected) {
// 	const audioFile = path.resolve(__dirname, '../../keywords', './heyGalileo2.wav')

//   let detector = new WakewordDetector({
// 		sampleRate: 16000,
//     threshold: 0.4
//   })

//   await detector.addKeyword('heyGalileo', [
//     './keywords/heyGalileo1.wav',
// 		'./keywords/heyGalileo2.wav',
// 		'./keywords/heyGalileo3.wav'
//   ], {
//     disableAveraging: true,
//     threshold: 0.4
//   })

//   detector.enableKeyword('heyGalileo')

//   detector.on('data', ({keyword, score, threshold, timestamp}) => {
// 		detected = true
//   })

// 	const detectionStream = new Stream.Writable({
//     objectMode: true,
//     write: (data, enc, done) => {
//       console.log(data)
//     }
//   })

//   detector.pipe(detectionStream)

// 	let stream = fileSystem.createReadStream(audioFile)
//   stream.pipe(detector)

//   setTimeout(() => {
//     stream.unpipe(detector)
//     stream.removeAllListeners()
//     stream.destroy()
//     stream = null

// 		detector.removeAllListeners()
// 		if (detected) {
// 			done()
// 		}
//   }, 4000)
// }
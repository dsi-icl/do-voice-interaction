const WakewordDetector = require('@mathquis/node-personal-wakeword')
const fs = require('fs')
const Stream = require('stream')
const path = require('path')
const url = require('url')

async function startListening(req, res) {
	if (req.body === null || req.body === undefined) {
		res.status(400).json({
			status: 'fail',
			service: 'Hotword service',
			message: 'The request body contains nothing'
		})
		return
	}

	getHotword(req.body, res)
}

async function getHotword(audioData, res) {
	const keywordClient = new WakewordDetector({
		sampleRate: 16000,
		threshold: 0
	})

	// Define keywords
	await keywordClient.addKeyword('heyGalileo', [
	  './keywords/heyGalileo1.wav',
		'./keywords/heyGalileo2.wav',
		'./keywords/heyGalileo3.wav',
		'./keywords/heyGalileo4.wav',
		'./keywords/heyGalileo5.wav',
		'./keywords/heyGalileo6.wav',
		'./keywords/heyGalileo7.wav',
		'./keywords/heyGalileo8.wav',
		'./keywords/heyGalileo9.wav',
	  './keywords/heyGalileo10.wav'
	], {
	  disableAveraging: true,
	  threshold: 0
	})

	keywordClient.enableKeyword('heyGalileo')

	keywordClient.on('ready', () => {
		console.log('Listening for hotword...')
	})

	// The detector will emit a "vad-silence" event when no voice is heard
  keywordClient.on('vad-silence', () => {
    console.log('Hearing silence...')
  })

  // The detector will emit a "vad-voice" event when it hears a voice
  keywordClient.on('vad-voice', () => {
    console.log('Hearing voices...')
  })

	keywordClient.on('error', err => {
		console.error(err.stack)
	})

	keywordClient.on('keyword', ({keyword, score, threshold, timestamp}) => {
		console.log(`Detected "${keyword}" with score ${score} / ${threshold}`)
		
		res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'detected'})
		return
	})

	const detectionStream = new Stream.Writable({
    objectMode: true,
    write: (data, enc, done) => {
      console.log(data)
      done()
    }
  })

  keywordClient.pipe(detectionStream)

	const filePath = path.resolve(__dirname, './keywords', './heyGalileo1.wav');
	const readStream = fs.createReadStream(filePath);
	// readStream.pipe(keywordClient)
	// console.log(readStream)

	// Compare the frame rate ...
	const buffer = Buffer.from(audioData, 'base64')
	//const readable = bufferToStream(buffer);

	// const newStream = new Readable({
	// 	read() {
	// 	  this.push(buffer);
	// 	},
	// })
	// console.log(newStream)
	// newStream.pipe(keywordClient)
	// var myReadableStreamBuffer = new streamBuffers.ReadableStreamBuffer({
	// 	frequency: 10,      // in milliseconds.
	// 	chunkSize: 2048     // in bytes.
	// }); 
	// myReadableStreamBuffer.put(buffer)
	// myReadableStreamBuffer.pipe(keywordClient)
	//myReadableStreamBuffer.stop()
	

	// const readable = new Stream.Readable()
	// readable._read = () => {} // _read is required but you can noop it
	// readable.push(buffer)
	// // readable.push(null)
	// readable.pipe(keywordClient)
	// console.log(readable)

	console.log('Hotword Service started successfully')
	res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'detected'})
	// res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'not-present'})
}

// function bufferToStream(myBuffer) {
//     let tmp = new Stream.Duplex();
//     tmp.push(myBuffer);
//     tmp.push(null);
//     return tmp;
// }

module.exports = {startListening, getHotword}
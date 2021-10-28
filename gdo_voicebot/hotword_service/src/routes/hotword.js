import WakewordDetector from '@mathquis/node-personal-wakeword'
import { ReadStream } from 'fs'
// import { Readable } from 'stream'
import Stream from 'stream'

import path from 'path';
import { fileURLToPath } from 'url';
import fileSystem from 'fs'

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function startListening(req, res) {
	if (req.body === null || req.body === undefined) {
		res.status(400).json({
			status: 'fail',
			service: 'Hotword service',
			message: 'The request body contains nothing'
		})
		return
	}

	// console.log("Body checks passed")
	getHotword(req.body, res)
	// keywordClient.emit('ready')
}

export async function getHotword(audioData, res) {
	const keywordClient = new WakewordDetector({
		// sampleRate: 16000,
		threshold: 0.5
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
	  threshold: 0.52
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
		// make api call to STT
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
	const readStream = fileSystem.createReadStream(filePath);
	readStream.pipe(keywordClient)
	console.log(readStream)

	const buffer = Buffer.from(audioData, 'base64')
	const readable = bufferToStream(buffer);
	// const readable = new Stream.Readable()
	// readable._read = () => {} // _read is required but you can noop it
	// readable.push(buffer)
	// // readable.push(null)
	// readable.pipe(keywordClient)
	console.log(readable)

	console.log('Hotword Service started successfully')
	setTimeout(() => {
		res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'Hotword Service responded successfully'})
  }, 5000)
}

function bufferToStream(myBuuffer) {
    let tmp = new Stream.Duplex();
    tmp.push(myBuuffer);
    tmp.push(null);
    return tmp;
}

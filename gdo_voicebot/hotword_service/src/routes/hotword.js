const WakewordDetector = require('@mathquis/node-personal-wakeword')
const fileSystem = require('fs')
const Stream = require('stream')
const path = require('path')

// Create the keyword client
const keywordClient = new WakewordDetector({
		sampleRate: 16000,
		threshold: 0.1
})

const maxSavedFiles = 10
let currentFileCount = 0

if (!fileSystem.existsSync('./config/config.json')) {
  console.error('Could not find the configuration file: \'./config/config.json\'')
  process.exit(1)
}

global.config = JSON.parse(fileSystem.readFileSync('./config/config.json').toString())

async function setUpKeywordClient(testing) {
	// Define keywords
	if (!testing) {
		await keywordClient.addKeyword(global.config.keyword.name, global.config.keyword.productionSamples, {
			disableAveraging: false,
			// threshold: 0.37
			threshold: 0.3
		})
	} else {
			await keywordClient.addKeyword(global.config.keyword.name, global.config.keyword.testSamples, {
			disableAveraging: false,
			threshold: 0.4
		})
	}

	keywordClient.enableKeyword(global.config.keyword.name)
}

async function startListening(req, res, testing=false) {
	if (req.body === null || req.body === undefined) {
		return res.status(400).json({
			status: 'fail',
			service: 'Hotword service',
			message: 'The request body contains nothing'
		})
	}

	return getHotword(req.body, res, testing)
}

async function getHotword(audioData, res, testing) {
	const buffer = Buffer.from(audioData, 'base64')
	const fileName = 'recording' + currentFileCount + '.wav'
	currentFileCount = (currentFileCount + 1) % maxSavedFiles

	if (!testing) {
		await fileSystem.writeFile('/app/save/' + fileName, buffer, function (err) {
			if (err) return console.log(err);
			console.log("Saved " + fileName);
		});
	}

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

	keywordClient.on('data', ({keyword, score, threshold, timestamp}) => {
		console.log(`Detected "${keyword}" with score ${score} / ${threshold}`)
		return res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'detected'})
	})

	const detectionStream = new Stream.Writable({
    objectMode: true,
    write: (data, enc, done) => {
      console.log(data)
      done()
    }
  })

  keywordClient.pipe(detectionStream)

  let filePath;
  if (!testing) {
  	filePath = path.resolve(__dirname, '/app/save/', fileName);
  } else {
		filePath = audioData;
  }
  const readStream = fileSystem.createReadStream(filePath);
  readStream.pipe(keywordClient)

	return res.status(200)
	// return res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'not-present'})
}

module.exports = {setUpKeywordClient, startListening, getHotword}
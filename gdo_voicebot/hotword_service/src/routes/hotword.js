const WakewordDetector = require('@mathquis/node-personal-wakeword')
const fileSystem = require('fs')
const Stream = require('stream')
const path = require('path')

// Check that the config file exists
if (!fileSystem.existsSync('./config/config.json')) {
  console.error('Could not find the configuration file: \'./config/config.json\'')
  process.exit(1)
}

// Get the config variables
global.config = JSON.parse(fileSystem.readFileSync('./config/config.json').toString())

// Create the keyword client from the Node-Personal-Wakeword third-party library
let keywordClient 

// The current file count where we will save the audio data
let currentFileCount = 0

// Track the previous audio data so that no file is saved twice
let prevAudioData

// Function that sets up the keyword client
async function setUpKeywordClient(testing) {
	keywordClient = new WakewordDetector({
		sampleRate: global.config.keyword.sampleRate,
		threshold: global.config.keyword.detectorThreshold
	})

	// Define keywords
	if (!testing) {
		await keywordClient.addKeyword(global.config.keyword.name, global.config.keyword.productionSamples, {
			disableAveraging: false,
			threshold: global.config.keyword.productionThreshold
		})
	}

	keywordClient.setMaxListeners(global.config.utils.listenersPerStream * global.config.utils.maxSavedFiles)
}

// Function which checks the arguements received and if so, it passes them forward to the getHotword method
async function startListening(req, res, testing = false, doneDetected = () => {}, doneRandom = ()=>{}) {
	if (req.body === null || req.body === undefined) {
		return res.status(400).json({
			status: 'fail',
			service: 'Hotword service',
			message: 'The request body contains nothing'
		})
	}

	getHotword(req.body, res, testing, doneDetected, doneRandom)
}

// Function which listens for the hotword in the given audio data using the third party library
async function getHotword(audioData, res, testing, doneDetected, doneRandom, detected=false) {
	// Discard the audio data if it has already been saved
	if (audioData === prevAudioData) {
		return res.status(200)
	}

	// Save the audio data as prevAudioData
	prevAudioData = audioData

	// The keyword client needs to be created every time a call is made as the library destroys it
	// after detecting a keyword (this happens in the close listener, after 'close' is emitted automatically) 
	// and hence we cannot reuse it for later detections
	setUpKeywordClient(testing)

	// Create a buffer from the audio data
	const buffer = Buffer.from(audioData, 'base64')

	// Get the file which should contain this data and update the currentFileCount
	const fileName = 'recording' + currentFileCount + '.wav'
	currentFileCount = (currentFileCount + 1) % global.config.utils.maxSavedFiles

	// Save the buffer into the file (not necessary if we are testing)
	if (!testing) {
		await fileSystem.writeFile('/app/save/' + fileName, buffer, function (err) {
			if (err) return console.log(err);
			console.log("Saved " + fileName);
		});
	}

	if (testing) {
		await keywordClient.addKeyword(global.config.keyword.name, global.config.keyword.testSamples, {
			disableAveraging: true,
			threshold: global.config.keyword.productionThreshold
		})
		keywordClient.enableKeyword(global.config.keyword.name)
	}

	// The detector will emit this message when it is ready
	keywordClient.on('ready', () => {
		if (!testing) {
			console.log('Listening for hotword...')
		}
	})

	keywordClient.on('error', err => {
		console.error(err.stack)
	})

	// When the keyword is detected, return the correct status and set the test to 'detected'
	keywordClient.on('data', ({keyword, score, threshold, timestamp}) => {
		console.log(`Detected "${keyword}" with score ${score} / ${threshold}`)
		detected = true
	})

	keywordClient.on('close', () => {
		console.log('Keyword destroyed in close listener - ', keywordClient.destroyed)
	})

	keywordClient.on('end', () => {
		console.log('Keyword destroyed in end listener - ', keywordClient.destroyed)
	})

	// Create a new detection stream for the keyword client and pipe it
	const detectionStream = new Stream.Writable({
    objectMode: true,
    write: (data, enc, done) => {
      console.log(data)
      done()
    }
  })
  keywordClient.pipe(detectionStream)

	// Get the filepath that needs to be piped and pipe it to the keyword client
  let filePath;
  if (!testing) {
  	filePath = path.resolve(__dirname, '/app/save/', fileName);
  } else {
	filePath = audioData;
  }
  let readStream = fileSystem.createReadStream(filePath);
  readStream.pipe(keywordClient)

	// Destroy the recorder and detector after 2s
  setTimeout(() => {
    readStream.unpipe(keywordClient)
    readStream.removeAllListeners()
    readStream.destroy()

	readStream = null

    keywordClient.removeAllListeners()
	if (detected) {
		doneDetected()
		res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'detected'})
	}
	if (!detected) {
		doneRandom()
		res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'not-detected'})
	}
  }, testing ? global.config.utils.testTimeoutValue : global.config.utils.timeoutValue)
}

module.exports = {setUpKeywordClient, startListening, getHotword}
const WakewordDetector = require('@mathquis/node-personal-wakeword')
const fileSystem = require('fs')
const Stream = require('stream')
const path = require('path')

// Create the keyword client from the Node-Personal-Wakeword third-party library
const keywordClient = new WakewordDetector({
		sampleRate: 16000,
		threshold: 0.1
})

// The current file count where we will save the audio data
let currentFileCount = 0

// Track the previous audio data so that no file is saved twice
let prevAudioData

// Check that the config file exists
if (!fileSystem.existsSync('./config/config.json')) {
  console.error('Could not find the configuration file: \'./config/config.json\'')
  process.exit(1)
}

// Get the config variables
global.config = JSON.parse(fileSystem.readFileSync('./config/config.json').toString())

// Function that sets up the keyword client and which is called when the service starts only
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
	keywordClient.setMaxListeners(3 * global.config.utils.maxSavedFiles)
}

// Function which checks the arguements received and if so, it passes them forward to the getHotword method
async function startListening(req, res, testing=false) {
	if (req.body === null || req.body === undefined) {
		return res.status(400).json({
			status: 'fail',
			service: 'Hotword service',
			message: 'The request body contains nothing'
		})
	}

	getHotword(req.body, res, testing)
}

// Function which listens for the hotword in the given audio data using the third party library
async function getHotword(audioData, res, testing) {

	// Discard the audio data if it has already been saved
	if (audioData === prevAudioData) {
		return res.status(200)
	}

	// Save the audio data as prevAudioData
	prevAudioData = audioData

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

	// The detector will emit this message when it is ready
	keywordClient.on('ready', () => {
		console.log('Listening for hotword...')
	})

	keywordClient.on('error', err => {
		console.error(err.stack)
	})

	// When the keyword is detected, return the correct status and set the test to 'detected'
	keywordClient.on('data', ({keyword, score, threshold, timestamp}) => {
		console.log(`Detected "${keyword}" with score ${score} / ${threshold}`)
		console.log('Removing all listeners ' + fileName)
		keywordClient.removeAllListeners()
		res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'detected'})
		return
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
  const readStream = fileSystem.createReadStream(filePath);
  readStream.pipe(keywordClient)

	// Destroy the recorder and detector after 2s
  setTimeout(() => {
    readStream.unpipe(keywordClient)
    readStream.removeAllListeners()
    readStream.destroy()

    keywordClient.removeAllListeners()
  }, 1000)
}

module.exports = {setUpKeywordClient, startListening, getHotword}
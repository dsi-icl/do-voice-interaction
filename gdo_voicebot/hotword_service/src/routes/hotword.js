const WakewordDetector = require('@mathquis/node-personal-wakeword')
const fileSystem = require('fs')
const Stream = require('stream')
const path = require('path')
const url = require('url')

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
	if (!testing) {
		fileSystem.writeFile('/app/save/helloworld.wav', buffer, function (err) {
			if (err) return console.log(err);
			console.log("Saved");
		});
	}

	const keywordClient = new WakewordDetector({
		sampleRate: 16000,
		threshold: 0.1
	})

	// Define keywords
	if (!testing) {
		await keywordClient.addKeyword('heyGalileo', [
			'./keywords/heyGalileoLiveVlad_no_silence.wav',

			'./keywords/heyGalileo1.wav',
			'./keywords/heyGalileo2.wav',    
			'./keywords/heyGalileo3.wav',
			'./keywords/heyGalileo4.wav',
			'./keywords/heyGalileo5.wav',    
			'./keywords/heyGalileo6.wav',
			'./keywords/heyGalileo7.wav',
			'./keywords/heyGalileo8.wav',    
			'./keywords/heyGalileo9.wav',
			'./keywords/heyGalileo11.wav',
			'./keywords/heyGalileo12.wav',    
			'./keywords/heyGalileo22.wav', 
			
			'./keywords/heyGalileoIza1.wav',
			'./keywords/heyGalileoIza2.wav',
			'./keywords/heyGalileoIza3.wav',
			'./keywords/heyGalileoIza7.wav',
			'./keywords/heyGalileoIza8.wav',
			'./keywords/heyGalileoIza9.wav',
		], {
			disableAveraging: false,
			// threshold: 0.37
			threshold: 0.3
		})
	} else {
			await keywordClient.addKeyword('heyGalileo', [
			'./keywords/heyGalileo1.wav'
		], {
			disableAveraging: false,
			threshold: 0.4
		})
	}

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
  	filePath = path.resolve(__dirname, '/app/save/', 'helloworld.wav');
  } else {
	filePath = audioData;
  }
  const readStream = fileSystem.createReadStream(filePath);
  readStream.pipe(keywordClient)

	return res.status(200)
	// return res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'not-present'})
}

module.exports = {startListening, getHotword}
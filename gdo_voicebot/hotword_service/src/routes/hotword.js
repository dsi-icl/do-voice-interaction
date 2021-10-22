import WakewordDetector from '@mathquis/node-personal-wakeword'

const keywordClient = new WakewordDetector({
    sampleRate: 48000,
    threshold: 0.5
})

export async function startListening(req, res) {
	if (req.body === null) {
		res.status(400).json({
			status: 'fail',
			service: 'Hotword service',
			message: 'The request body contains nothing'
		})
		return
	}

	getHotword(req.body)
	keywordClient.emit('ready')

	console.log('Hotword Service started successfully')
	res.status(200).json({ status: 'ok', service: 'Hotword service', text: 'Hotword Service started successfully'})
}

async function getHotword(audioData) {
	keywordClient.on('ready', () => {
		console.log('Listening for hotword...')
	})

	keywordClient.on('error', err => {
		console.error(err.stack)
	})

	keywordClient.on('keyword', ({keyword, score, threshold, timestamp, audioData}) => {
		console.log(`Detected "${keyword}" with score ${score} / ${threshold}`)
		// make api call to STT
	})

	// Define keywords
	// await keywordClient.addKeyword('abrakadabra', [
	//     './keywords/abrakadabra1.wav',
	//     './keywords/abrakadabra2.wav'
	// ], {
	//     disableAveraging: true,
	//     threshold: 0.52
	// })

	// keywordClient.enableKeyword('abrakadabra')

	// const buffer = Buffer.from(req.body, 'base64')
	
	// keywordClient.once('ready', () => {
	// 	console.log('Discord Client Loaded!');
	// });

	// const context = new AudioContext();
	// const source = context.createMediaStreamSource(stream);
	// const processor = context.createScriptProcessor(1024, 1, 1);

	// source.connect(processor);
	// processor.connect(context.destination);

	// processor.onaudioprocess = function(e) {
	//   // Do something with the data, e.g. convert it to WAV
	//   console.log(e.inputBuffer);
	// };
}

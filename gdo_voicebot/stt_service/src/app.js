/**
 * @file Manages routing for the Speech-To-Text service
 * @author Aurélie Beaugeard
 */

import express from 'express'
import cors from 'cors'
import logger from 'morgan'
import fs from 'fs'

/**
 * @import { loadDeepSpeechModel, executeSpeechToTextRequest } from "./routes/stt.js"
 * @see {@link ./routes/stt.js|stt.js}
 */
import { executeSpeechToTextRequest, loadDeepSpeechModel } from './routes/stt.js'

/**
 * @import { sampleData } from "./routes/index.js"
 * @see {@link "./routes/index.js"|index.js}
 */
import { sampleData } from './routes/index.js'

if (!fs.existsSync('./config/config.json')) {
  console.error('Could not find the configuration file: \'./config/config.json\'')
  process.exit(1)
}

global.config = JSON.parse(fs.readFileSync('./config/config.json').toString())

const app = express()

// Generate the deepspeech model and if it fails, returns the error to the server console
let model
try {
  model = loadDeepSpeechModel()
} catch (error) {
  console.error('Error during deepspeech model construction')
  console.error(error)
  process.exit(2)
}

app.use(cors())
app.use(logger('dev'))
// Has been added to enable audio blob transfers
app.use(express.text({ limit: '50mb' }))
app.use(express.urlencoded({ extended: false }))

/**
 * Get service status
 *
 * @name Getting service status
 * @route {GET} /api/status
 */
app.get('/api/status', (req, res) => res.send('Service is running'))

/**
 * Test service with simple json response
 *
 * @name Getting the test result
 * @route {GET} /api/json
 */
app.get('/api/json', sampleData)

/**
 * Get the speech to text transcription using the received audio blob
 *
 * @name Speech-To-Text transcription post
 * @route {POST} /api/stt
 * @headerparam Content-type must be text/plain
 */
app.post('/api/stt', (req, res) => { executeSpeechToTextRequest(req, res, model) })

export default app

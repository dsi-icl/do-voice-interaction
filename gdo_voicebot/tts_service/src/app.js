/**
 * @file Manages routing of the text-to-speech service
 * @author Aurélie Beaugeard
*/

import express from 'express'
import cors from 'cors'
import logger from 'morgan'
import fs from 'fs'

/**
 * @import { sampleData } from "./routes/index.js"
 * @see {@link "./routes/index.js"|index.js}
 */
import { sampleData } from './routes'

import { textToSpeech } from './routes/tts.js'

if (!fs.existsSync('./config/config.json')) {
  console.error("Could not find the configuration file: './config/config.json'")
  process.exit(1)
}

global.config = JSON.parse(fs.readFileSync('./config/config.json').toString())

const app = express()

app.use(cors())
app.use(logger('dev'))
app.use(express.json())
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
 * Text to Speech service
 *
 * @name Text to Speech service
 * @route {GET} /api/tts
 * @see {@link https://www.npmjs.com/package/gtts|Gtts}
 */
app.get('/api/tts', (req, res) => { textToSpeech(req, res) })

export default app

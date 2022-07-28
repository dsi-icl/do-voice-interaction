/**
 * @file Manages routing of the text-to-speech service
 * @author Aurélie Beaugeard
 */


import express from 'express'
import cors from 'cors'
import logger from 'morgan'
import fs from 'fs'

import {setupEngine, textToSpeech } from './routes/tts.js'


if (!fs.existsSync('./config/config.json')) {
  console.error('Could not find the configuration file: \'./config/config.json\'')
  process.exit(1)
}
global.config = JSON.parse(fs.readFileSync('./config/config.json').toString())

setupEngine()

const app = express()

app.use(cors())
app.use(logger('dev'))
app.use(express.json({ limit: '50mb' }))
app.use(express.urlencoded({ extended: false }))
/**
 * Get service status
 *
 * @name Getting service status
 * @route {GET} /api/status
 */
app.get('/api/status', (req, res) => res.status(200).send('Service is running'))

/**
 * Text to Speech service
 *
 * @name Text to Speech service
 * @route {GET} /api/tts
 * @see {@link https://www.npmjs.com/package/gtts|Gtts}
 */
// app.get('/api/tts', textToSpeech)
app.post('/api/tts', textToSpeech)

export default app

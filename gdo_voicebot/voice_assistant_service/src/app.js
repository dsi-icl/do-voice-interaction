/**
 * @file Manages routing of the voice-assistant service and socket communication with the client
 * @author Aurélie Beaugeard
 */

import express from 'express'
import cors from 'cors'
import logger from 'morgan'
import fs from 'fs'
import path from 'path'
import favicon from 'serve-favicon'

import { processAudioHotword, processAudioCommand, processTextCommand } from './routes/voice_assistant.js'

if (!fs.existsSync('./config/config.json')) {
  console.error('Could not find the configuration file: \'./config/config.json\'')
  process.exit(1)
}

global.config = JSON.parse(fs.readFileSync('./config/config.json').toString())

const app = express()
const __dirname = path.resolve()

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
app.get('/api/status', (req, res) => res.send('Service is running'))

app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')))
app.use('/', express.static(path.join(__dirname, 'public')))

/**
 * Function that manage the entire communication process between the server and the client
 * @param {SocketIO.Client} client The client with which the server communicates
 */
export function setupClient (client) {
  console.log('Client connected\n')

  client.on('audio-hotword', (request) => processAudioHotword(client, request))
  client.on('audio-command', (request) => processAudioCommand(client, request))
  client.on('text-command', (request) => processTextCommand(client, request))
}

export default app

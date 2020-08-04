/**
 * @file Manages routing of the voice-assistant service and socket communication with the client
 * @author Aurélie Beaugeard
*/

import express from 'express'
import cors from 'cors'
import logger from 'morgan'
import fs from 'fs'
import http from 'http'
import path from 'path'
import socketio from 'socket.io'

/**
 * @import { sampleData, postData, getData } from "./routes/index.js"
 * @see {@link "./routes/index.js"|index.js}
 */
import { sampleData } from './routes/index.js'
import { echoProcess } from './routes/voice_assistant.js'

if (!fs.existsSync('./config/config.json')) {
  console.error("Could not find the configuration file: './config/config.json'")
  process.exit(1)
}

global.config = JSON.parse(fs.readFileSync('./config/config.json').toString())

const app = express()
var httpServer = http.createServer(app)
const __dirname = path.resolve()

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

app.use('/node_modules', express.static(path.join(__dirname, '/node_modules')))
/**
 * To serve static files such as images, CSS files, and JavaScript files, use the express.static built-in middleware function in Express.
 *
 * @name Serving static files in Express
 * @route {USE} /api/echo
 * @see {@link https://expressjs.com/en/starter/static-files.html|Exprees}
 */
app.use('/api/echo', express.static('public'))

httpServer.listen(2000, () => {
  console.log('listening on *:2000\n')
})

// instanciation of a socket listening to the httpServer connected to the app
var io = socketio.listen(httpServer)

io.on('connect', (client) => { echoProcess(client) })

export default app

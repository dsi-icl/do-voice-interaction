const express = require('express')
const hotwordService = require('./routes/hotword.js')
const fs = require('fs')

const app = express()

app.use(express.text({ limit: '50mb' }))
app.use(express.urlencoded({ extended: false }))

if (!fs.existsSync('./config/config.json')) {
  console.error('Could not find the configuration file: \'./config/config.json\'')
  process.exit(1)
}

global.config = JSON.parse(fs.readFileSync('./config/config.json').toString())

/**
 * Get service status
 *
 * @name Getting service status
 * @route {GET} /api/status
 */
app.get('/api/status', (req, res) => res.status(200).json({ status: 'ok', service: 'Hotword service', text: "Hotword Service Active" }))

/**
 * Listen for hotword using the received audio blob
 *
 * @name Start-Listening notify on hotword detection
 * @route {POST} /api/hotword
 * @headerparam Content-type must be text/plain
 */
app.post('/api/hotword', (req, res) => { hotwordService.startListening(req, res) })

export default app

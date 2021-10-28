import express from 'express'
// import cors from 'cors'
// import logger from 'morgan'

import { startListening, getHotword } from './routes/hotword.js'

const app = express()

// app.use(cors())
// app.use(logger('dev'))
/* Has been added to enable audio blob transfers */
app.use(express.text({ limit: '50mb' }))
app.use(express.urlencoded({ extended: false }))

// app.get('/', getHotword)

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
app.post('/api/hotword', (req, res) => { startListening(req, res) })

export default app

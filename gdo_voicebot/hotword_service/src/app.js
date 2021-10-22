import express from 'express'
// import cors from 'cors'

import { startListening } from './routes/hotword.js'

const app = express()

// app.use(cors())

app.get('/api/status', (req, res) => res.status(200).json({ status: 'ok', service: 'Hotword service', text: "Hotword Service Active" }))
app.post('/api/hotword', (req, res) => startListening(req, res))

export default app

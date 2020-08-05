const Gtts = require('gtts')

/**
 * Function that execute text to speech service get request
 * @param {Request} req The received request from the voice-assistant service
 * @param {Response} res The response to be sent to the voice-assistant service in stream format
 * @see {@link https://www.npmjs.com/package/gtts|Gtts}
 */
export function textToSpeech (req, res) {
  try {
    const gtts = new Gtts(req.query.text, req.query.lang)
    gtts.stream().pipe(res)
  } catch(err){
    res.status(400).json({status: 'fail', service: 'Text To Speech  service', message: err.toString() })
  }
  
}

/**
 * @file Manages some deepspeech utilities functions
 * @author Aurélie Beaugeard
*/

/**
 * This function returns a json response to be sent at the /api/json route.
 *
 * @param {Request} req The user's request
 * @param {Response} res The service response
 */
export function sampleData (req, res) {
  res.json({ data: 'sampleData' })
}

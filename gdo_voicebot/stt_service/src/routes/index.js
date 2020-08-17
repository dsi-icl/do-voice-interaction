/**
 * @file Manages some utilities functions
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

/**
 * This function checks if any object is empty.
 *
 * @param {Object} obj The object to be checked
 * @returns {Boolean} The boolean value
 */
export function isEmpty (obj) {
  for (let key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) { return false }
  }
  return true
}

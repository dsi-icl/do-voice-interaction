/**
 * @file Manages some utilities functions
 * @author Aurélie Beaugeard
*/

/**
 * This function checks if any object is empty.
 *
 * @param {Object} obj The object to be checked
 * @returns {Boolean} The boolean value
 */
export function isEmpty (obj) {
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) { return false }
  }
  return true
}

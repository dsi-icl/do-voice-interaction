/**
 * Function to merge url parameters
 * @param {Url} url The url from the request
 * @param {Object} params The request parameters contained in a dictionnary
 */
export function mergeUrlParams (url, params) {
  const result = new URL(url)
  Object.keys(params).forEach(key => result.searchParams.append(key, params[key]))
  return result
}

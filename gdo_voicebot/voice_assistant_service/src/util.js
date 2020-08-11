
//todo; document this function
export function mergeUrlParams (url, params) {
  const result = new URL(url)
  Object.keys(params).forEach(key => result.searchParams.append(key, params[key]))
  return result
}
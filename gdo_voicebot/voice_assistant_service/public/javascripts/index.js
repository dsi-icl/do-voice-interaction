/**
 * @file Manages utils functions used by the client
 * @author Aurélie Beaugeard
*/

var hark = require("../hark.ks");

/**
 * Function that instanciated and return a hark object
 * 
 * @param {Stream} stream The navigator stream
 * @param {Options} options The options that can be added : interval, threshold, play, audioContext
 * @returns {Hark} The hark object
 * @see{@link https://www.npmjs.com/package/hark|hark}
 * @see{@link https://github.com/otalk/hark|Hark}
 */
function Hark(stream,options){
    return hark(stream,options);
}

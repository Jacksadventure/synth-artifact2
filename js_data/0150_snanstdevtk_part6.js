/**
* Computes the standard deviation of a single-precision floating-point strided array ignoring `NaN` values and using a one-pass textbook algorithm.
*
* @param {PositiveInteger} N - number of indexed elements
* @param {number} correction - degrees of freedom adjustment
* @param {Float32Array} x - input array
* @param {integer} stride - stride length
* @returns {number} standard deviation
*
* @example
* var Float32Array = require( '@stdlib/array/float32' );
*
* var x = new Float32Array( [ 1.0, -2.0, NaN, 2.0 ] );
*
* var v = snanstdevtk( x.length, 1, x, 1 );
* // returns ~2.0817
*/
function snanstdevtk( N, correction, x, stride ) {
	return float64ToFloat32( sqrt( snanvariancetk( N, correction, x, stride ) ) ); // eslint-disable-line max-len
}
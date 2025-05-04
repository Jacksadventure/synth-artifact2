// A library for performing various math operations
export const Math = {
    // Define your math functions or constants here
  };
  
const MathLibrary = {
    min: function(x, y) {
        return x < y ? x : y;
    },

    // Babylonian method (https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Babylonian_method)
    sqrt: function(y) {
        if (y > 3) {
            let z = y;
            let x = Math.floor(y / 2) + 1;
            while (x < z) {
                z = x;
                x = Math.floor(y / x + x) / 2;
            }
            return Math.floor(z);
        } else if (y !== 0) {
            return 1;
        } else {
            return 0;
        }
    }
};

module.exports = MathLibrary;

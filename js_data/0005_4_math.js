"use strict";
// Math is an object in JavaScript
console.log(Math.abs(-4)); // 4: makes a value absolute

console.log(Math.round(4.6)); // 5: rounds off the value
console.log(Math.ceil(4.2)); // 5: ceil refers to the top, means as the value is above 4 it will output 4
console.log(Math.floor(4.9)); // 4: floor used until the value is not greater than another integer
console.log(Math.sqrt(25)); // 5
console.log(Math.pow(5, 2)); // 25

console.log(Math.min(1, 2, 3, 4, 5)); // Prints the minimum value in the array
console.log(Math.max(2, 3, 4, 7, 8, 9, 10)); // Prints the maximum value in the array

// Math library mostly used for Math.random
console.log(Math.random()); // Its value ranges from 0 to 1
console.log(Math.floor(Math.random() * 10 + 1));

const min = 10;
const max = 20;
console.log(Math.floor(Math.random() * (max - min + 1)) + min);

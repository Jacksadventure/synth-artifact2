//Arrays
//Arrays are ordered collections of elements that can hold various data types in JavaScript. They are a fundamental data structure and provide an efficient way to store and manage lists of items.
//creating and accessing elements in array
const computers = ["Apple", "HP", "Mac"];
console.log(computers[0]);

// array manipulation
const sports = ["football", "table tenis", "cricket"];
sports[1] = "swimming";
console.log(sports[1]);

//Create an array of numbers and print the sum of all elements using a loop:
const numbers = [10, 2, 35, 44, 52];
let total = 0;

for (let i = 0; i < numbers.length; i++) {
  total += numbers[i];
}

console.log(total);

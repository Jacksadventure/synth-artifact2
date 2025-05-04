"use strict";

// DESCRIPTION:
// Write a function reverse which reverses a list (or in clojure's case, any list-like data structure)

// (the dedicated builtin(s) functionalities are deactivated)

// Test Cases:
// describe("Tests", () => {
//   it("test", () => {
//     assert.deepEqual(reverse([1, 2, 3]), [3, 2, 1]);
//     assert.deepEqual(reverse([1, null, 14, "two"]), ["two", 14, null, 1]);
//   });
// });

const reverse = function (array) {
  // TODO: program me!
  //   return array.reverse();
  let output = [];
  for (let i = array.length - 1; i >= 0; i--) {
    output.push(array[i]);
  }
  return output;
};

console.log(reverse([1, 2, 3]));
console.log(reverse([1, null, 14, "two"]));
console.log(reverse([55, 365, 761]));

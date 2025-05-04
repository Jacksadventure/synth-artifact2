// Use typeof to Check the Type of a Variable
// You can use typeof to check the data structure, or type, of a variable. 
// This is useful in debugging when working with multiple data types. 
// If you think you're adding two numbers, but one is actually a string, the results can be unexpected. 
// Type errors can lurk in calculations or function calls. Be careful especially when you're accessing and working with external data in the form of a JavaScript Object Notation (JSON) object.

let seven = 7;
let three = "3";
console.log(seven + three);
// Only change code below this line
console.log(typeof(seven))
console.log(typeof(three))

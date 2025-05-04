// these are not the number operations they are maths library operations 


console.log(Math.abs(-4)); //keeps values absolute positive
console.log(Math.round(4.5)); //rounds off the value
console.log(Math.ceil(4.3));//rounds off to maximum closest number
console.log(Math.floor(4.8));//rounds off to minimum closest number
console.log(Math.min(3,4,5,1));//finds out minimum value in an array
console.log(Math.max(3,4,5,1));//finds out maximum value in an array

console.log(Math.random());//generates random number from 0-1 like 0.1, 0.3
console.log(Math.random()*10);// to get values from 1-10 but i can generate 0 also
console.log(Math.floor(Math.random()*10)+1); //this will not give 0 floor removes the decimal point

// //but if u want to customize the random value you want o generate within a limit

let min = 10;
let max = 20;

console.log(Math.floor(Math.random()*(max-min + 1))+min);//sets the max and min value it wont cross

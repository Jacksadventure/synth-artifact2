// Inbuild functions used with arrays in JS 
// 3 functions map, reduce, filter are in built fuction
// IN built function is a pre defined fucntion which doesn't need to pass logic
// map, reduce, filter is also a higher order function which takes another function as its parameter
const numbers = [4,9,16,25];
const newArr = numbers.map(Math.sqrt)
console.log(newArr);
// sqrt is a in built function in Math library

const numbers1 = [65,44,12,4];
const newArr1 = numbers1.map(myfunction)

function myfunction(num){
    return num * 10
}
console.log(newArr1);
//map ()function doesnt change the original array

const persons = [
    {firstname: "Balaji",lastname:"Lakshmanan"},
{firstname: "Kapil", lastname: "Dev"},
{firstname:"Lionel",lastname:"Messi"}
];
persons.map(getFullName);
// const newarr2 = persons.map(getFullName);

function getFullName (item){
 // return item.firstname+" "+item.lastname
     return [item.firstname,item.lastname].join(" ");
}
console.log(getFullName);
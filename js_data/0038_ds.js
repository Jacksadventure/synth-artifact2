/*              Practise for Data Structure and Logic
let arr = [-5, -4, -3, -2, 0, 2, 4, 6, 8];

function findSumPair(arr) {
  let left = 0;
  let right = arr.length - 1;

  while (left < right) {
    sum = arr[left] + arr[right];
    if (sum == 0) {
      return [arr[left], arr[right]];
    } else if (sum > 0) {
      right--;
    } else {
      left++;
    }
  }
}

const result = findSumPair([-5, -4, -3, -2, 0, 2, 4, 6, 8]);
console.log("This is the pair, whose sum is zero", result);         */

// Callback function

function calculator(num1, num2, callback) {
  let sum = num1 + num2;
  callback(sum);
}

calculator(5, 5, function (result) {
  console.log(result);
});

//Update///////

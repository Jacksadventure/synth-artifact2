//input/output: two number arrays / array comprised of the product of each pair
//              of same-indexed numbers from the input arrays
//rules: - the input arrays will have the same length
//data structures: array, loop with count
//algorithm:
//START
//SET products array
//SET count = 0
//WHILE count < the length of one of the input arrays
//  push the result of multiplying the number at index count from both arrays
//  to the products array
//PRINT products
//END

function multiplyList(nums1, nums2) {
  let products = [];
  for (let i = 0; i < nums1.length; i++) {
    products.push(nums1[i] * nums2[i]);
  }
  return products;
}

multiplyList([3, 5, 7], [9, 10, 11]);    // [27, 50, 77]
multiplyList([], []); // []
multiplyList([1], [0]); // [0]
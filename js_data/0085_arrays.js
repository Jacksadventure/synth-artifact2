const arr = [0,1,2,3,4,5,6,7,true,'ambivert']

console.log(arr[0]);

// Array make shallow copies of an object 

/* Shallow Copy -: Follows heap data structure 

instead of saving the object to another variable shallow 
copy points the new variable to the original array/object.

This means that whenever you change any value in the another variable
it is going to reflect back in all the copies of the object/array you have created.



Deep Copy -: Follows stack data Structure

The new variable store the value/datac into a stack and 
any changes made into the new variable does not affect 
the value in the original variable and all 
the other copies of the data/value .


*/
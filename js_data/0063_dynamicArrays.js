// # Concept Drills: Arrays & Sorting

// ## Arrays

// Arrays are data structures that store content with contiguous blocks of memory
// The fact that the memory is contiguous allows us to know where any item in the array is in constant time as long as we have the starting memory address and the index

// - key in and fetch an item from an array in O(1) given the index
// - O(N) to add an item to an array anywhere but the back
// - O(1) to push an item to the back of an array
// - same thing for removing ^
// - Doubling the size of a dynamic array is amortized to constant time

class DynamicArray {
	constructor() {
		this.store = [];
		this.length = 0;
		this.maxSize = 4;
	}

	push(item) {
		if (this.length === this.maxSize) {
			this.maxSize = 2 * this.maxSize;
		}

		this.store.push(item);
		this.length++;
	}

	pop() {
		this.length--;
		return this.store.pop();
	}

	get(idx) {
		if (idx >= this.length) {
			return null;
		}
		return this.store[idx];
	}
}

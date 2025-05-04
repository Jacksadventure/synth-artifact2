// While not directly related to React, having a good understanding of data structures and algorithms can help in writing efficient and scalable React code, especially when dealing with complex state management or performance-critical components
// Example of a simple stack data structure
class Stack {
  constructor() {
    this.items = [];
  }

  push(element) {
    this.items.push(element);
  }

  pop() {
    if (this.items.length === 0) return "Underflow";
    return this.items.pop();
  }

  peek() {
    return this.items[this.items.length - 1];
  }
}

class ListNode {
  constructor(value = null) {
    this.next = null;
    this.value = value;
  }
}

class MyStack {
  constructor() {
    // TODO: Constructor of the Stack MyStack
  }

  push(value = null) {
    // TODO: Push function for the Stack Data Structure
    // If the value is null or not a digit should not push
  }

  pop() {
    // TODO: Pop function for the Stack Data Structure
  }

  toArray() {
    // TODO: Convert the stack into array.
    // If Stack has pushed, in order, 0 1 2. The returned array should be [2,1,0]
  }
}

module.exports = MyStack;

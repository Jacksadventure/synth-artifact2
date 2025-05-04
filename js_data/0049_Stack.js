/**
 * This is an array implementation of a Stack,
 * which is a LIFO linear data structure.
 * @template T - the type of element stored in the stack
 */
class Stack {
  /**
   * Creates a Stack with optional initial elements.
   * @param {T[]} arr
   */
  constructor(arr = []) {
    this.arr = arr;
  }

  /**
   * Adds `element` to the top of the stack.
   * @param {T} element
   */
  push(element) {
    // TODO
  }

  /**
   * Removes and returns the element at the top of the stack,
   * or `undefined` if the stack is empty.
   * @returns {T|undefined}
   */
  pop() {
    // TODO
  }

  /**
   * Returns the element at the top of the stack _without_ removing it,
   * or undefined if the stack is empty.
   * @returns {T|undefined}
   */
  peek() {
    // TODO
  }

  /** @returns {boolean} whether the stack is empty. */
  isEmpty() {
    // TODO
  }

  /** @returns {number} the number of elements in the stack. */
  size() {
    // TODO
  }
}

module.exports = Stack;

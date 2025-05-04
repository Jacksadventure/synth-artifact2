/**
 * This is an array implementation of a Queue,
 * which is a FIFO linear data structure.
 * @template T - the type of element stored in the queue
 */
class Queue {
  /**
   * Creates a Queue with optional initial elements.
   * @param {T[]} arr
   */
  constructor(arr = []) {
    this.arr = arr;
  }

  /**
   * Adds `element` to the back of the queue
   * @param {T} element
   */
  enqueue(element) {
    // TODO
  }

  /**
   * Removes and returns the element at the front of the queue,
   * or `undefined` if the queue is empty.
   * @returns {T|undefined}
   */
  dequeue() {
    // TODO
  }

  /**
   * Returns the element at the front of the queue _without_ removing it,
   * or undefined if the queue is empty.
   * @returns {T|undefined}
   */
  peek() {
    // TODO
  }

  /** @returns {boolean} whether the queue is empty. */
  isEmpty() {
    // TODO
  }

  /** @returns {number} the number of elements in the queue */
  size() {
    // TODO
  }
}

module.exports = Queue;

/**
 * Initialize your data structure here.
 */
class MyHashSet {
  constructor() {
    this.buckets = [];
  }
  /**
   * @param {number} key
   * @return {void}
   */
  add(key) {
    this.buckets[key] = key;
  }
  /**
   * @param {number} key
   * @return {void}
   */
  remove(key) {
    this.buckets[key] = undefined;
  }
  /**
   * Returns true if this set contains the specified element
   * @param {number} key
   * @return {boolean}
   */
  contains(key) {
    return this.buckets[key] !== undefined;
  }
}




/** 
 * Your MyHashSet object will be instantiated and called as such:
 * var obj = new MyHashSet()
 * obj.add(key)
 * obj.remove(key)
 * var param_3 = obj.contains(key)
 */
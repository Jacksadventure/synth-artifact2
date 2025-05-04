/*********************************** Bracket matcher
 * In this example we will match brackets(only parenthesis) weather they are valid or invalid
 * by using the logic of "alvin" youtube channel guy "coder-byte".
 * by using stack data structure concept (FILO);
 * return 0 if it is invalid else 1
 */

function bracketMatcher(str) {
  let stack = [];
  for (let i = 0; i < str.length; i++) {
    if (str[i] === "(") {
      stack.push("(");
    } else if (str[i] === ")") {
      if (stack.length === 0) {
        return false;
      } else {
        stack.pop();
      }
    }
  }
  return stack.length === 0 ? true : false;
}
console.log(bracketMatcher("((()))"));
// both time complexity & space complexity are O(n)

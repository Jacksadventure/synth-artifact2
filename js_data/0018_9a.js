// Modular Math: Let's create a reusable math library. 
// In a file named math.js, define functions for addition, subtraction, multiplication, and division.
//  In your main application file (e.g., app.js),
//   import the necessary functions from math.js and use them to perform calculations.

class maths{
    constructor(a,b){
        this.a = a,
        this.b = b
    }
    addition(){
        return this.a + this.b
    }
    subtraction(){
        return this.a - this.b
    }
    multiplication (){
        return this.a *this.b
    }
    division(){
        return this.a / this.b
    }
}
module.exports = maths


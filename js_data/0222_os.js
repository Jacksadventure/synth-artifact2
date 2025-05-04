// 2.a.) The os module provides a number of operating system-related utility methods. It appears to be very useful in providing the developer with information about the operating system on which the Node.js application is running. It can be accessed from anywhere in a Node.js application.

// 2.b.)

const os = require("os");

// logs to the console the operating system platform
console.log(os.platform());

// logs to the console the operating system name
console.log(os.type());

// logs to the console the operating system release
console.log(os.release());

// logs to the console information about each CPU core
console.log(os.cpus());

// logs to the console the total memory of the system
console.log(os.totalmem());

// logs to the console the amount of free memory of the system
console.log(os.freemem());

// logs to the console an object containing network interfaces that have been assigned a network address
console.log(os.networkInterfaces());

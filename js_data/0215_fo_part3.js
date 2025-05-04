
//process.argv property returns an array containing the command-line arguments passed when the Node.js process was launched.
// The first item (argv[0]) will be the path to node itself, and the second item (argv[1]) will be the path to your script code.
//So a slice starting at 2 will discard both of those and return everything else that was typed on the command line. These are the arguments that will be used to construct the API query string.
let input = process.argv.slice(2);//it takes the input
let command = input[0];
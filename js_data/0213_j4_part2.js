/*
 * A J4 Compiler
 *
 * This is a command line application that compiles a J4 program from
 * a file. There are three options:
 *
 * ./j4.js -a <filename>
 *     writes out the AST and stops
 *
 * ./j4.js -i <filename>
 *     writes the decorated AST then stops
 *
 * ./j4.js <filename>
 *     compiles the J4 program to JavaScript, writing the generated
 *     JavaScript code to standard output.
 *
 * ./j4.js -o <filename>
 *     optimizes the intermediate code before generating target JavaScript.
 *
 * NOTE FOR WINDOWS USERS: node j4.js -i filename.js
 * This is an example of how you should run this on windows command prompt
 * NOTE you can pipe output directly into node to run directly
 *
 * Output of the AST and decorated AST uses the object inspection functionality
 * built into Node.js.
 */
const soundsDir = "./SoundClips";
const player = require("play-sound")({});
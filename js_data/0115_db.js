const pgp = require('pg-promise')();

const cn = {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    database: process.env.DB_NAME,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD
};

const db = pgp(cn);

module.exports = db;

// db.any('SELECT * FROM story', [true])
//     .then(function(data) {
//         console.log(datassigns module.exports to a different object or different data structure, then any a);
//         // success;
//     })
//     .catch(function(error) {
//         // error;
//         console.log(error)
// });
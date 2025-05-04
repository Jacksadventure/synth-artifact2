// read environment variables for rds db connection, env vars are read from .env file, which is created in codedeploy appspec workflow.
// the originial env vars come from user data in launch configuration, values were set when infrastructures were created by Terrafrom

module.exports = {
    HOST: process.env.RDS_HOSTNAME,
    USER: process.env.RDS_USERNAME,
    PASSWORD: process.env.RDS_PASSWORD,
    DB: process.env.RDS_DATABASE,
    PORT: process.env.RDS_PORT,
    dialect: "mysql",
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000,
    },
  }
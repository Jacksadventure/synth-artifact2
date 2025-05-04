//this class will be used to create structured error objects

class ApiError extends Error {
    constructor(statusCode, message="Something went wrong", errors=[], stack="") {
        super(message); //this actually makes it an Error
        this.statusCode = statusCode;
        this.message = message;
        this.errors = errors;
        this.data = null;
        this.success = false

        this.stack = stack ? stack : Error.captureStackTrace(this, this.constructor);
    }
}

module.exports = ApiError;
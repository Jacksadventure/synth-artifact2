'use strict';
// a program that sends messages is a producer
// a queue is a data structure that can contain an infinite amount of messages
// a consumer is a program that waits for messages to be ready to consume from the queue
// after locally installing the RabbitMQ server; you can start it up and then kill it when you're done with it
// a queue is created on the RabbitMQ server and the producer service publishes messages to it and a consumer subscribes to that queue in hopes of receiving messages from it

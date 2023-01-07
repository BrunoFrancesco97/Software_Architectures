# Task 4 Documentation

## Requirements
For this task is asked to build up an Hackerrank-like application over a distributed architecture, Task 3 monolithic application is used as starting point.

## Overview of the architecture

Since requirements ask for a distributed architecture, the original application is now splitted into different services that can be placed inside different communicating machines (in order to simplify life professor, we build a simulation of a distributed architecture so a unique docker compose is used as final artifact).

![Alt Image text](/Task%204/img/distributed.png "Application structure")

Application is still layered (frontend and backend), so there is a monolithic frontend where all HTTP requests are made. These requests are sent to the API gateway/layer, the first part of the backend a user encounter.

This gateway is very important since is a proxy to the right microservice but also it handles the login/logout services through JWT cookie (see Task 3 for a better explaination of this technology).

So, when the gateway has choosen the right microservice to send the request, it starts a synchronous communication and wait for a response, when this one is received then is sent back to the user.

Image above shows how the architecture is built, arrows from the api gateway to the microservices are missing since if they were present, image would be very messy but as I said above, gateway to microservices communication is handled by a synchronous stream.

## Backend
As shown above, there are several microservices used on our application, the granularity used for splitting them was chosen by considering the resources each microservice would have operated with, so microservices implemented are:
- _assignment_: microservice used to add and remove an assignment;
- _channel_: microservice used to get, add and remove a channel;
- _course_: microservice used to get, add and remove a course;
- _exercise_: microservice used to get, create and answer to an exercise;
- _file_: microservice used to add and remove a file inside a course;
- _filesystem:
- _loginreg_: microservice used to registrate or login a user;
- _message_; microservice used to get or send messages; 
- _result_: microservice used to get assignments results;
- _solution_: microservice used to get or add a solution to an exercise; 
- _subscription_: microservice used to get or add a subscription to a channel or course;
- _test_: microservice used to get or add tests related to an exercise;
- _user_: microservice used to get user information;

### Microservices
#### API Layer 
### RabbitMQ
### Databases

## How to run 

## Test it

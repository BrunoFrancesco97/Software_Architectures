# Task 4 Documentation

## Requirements
For this task is asked to build up an Hackerrank-like application over a distributed architecture, Task 3 monolithic application is used as starting point.

## Overview of the architecture used

Since requirements ask for a distributed architecture, the original application is now splitted into different services that can be placed inside different communicating machines (in order to simplify life professor, we build a simulation of a distributed architecture so a unique docker compose is used as final artifact), in detail our application is based on *microservices*.

![Alt Image text](/Task%204/img/distributed.png "Distributed architecture")

Application is still layered so there is a monolithic frontend where all HTTP requests are made and a backend, no more a monolithic one. These requests made from the frontend are sent to the API gateway/layer, the first part of the backend a user encounter.

## Backend
#### API Layer 
API layer is the first component met by a user inside backend and is very important since is a proxy to the right microservice but also it handles the login/logout services through JWT cookie (see Task 3 for a better explaination of this technology).

A user can send requests to the API layer thanks to a list of fixed endpoints that are the same as task 3 ones so for space reasons they are omitted from being displayed here (see Task 3 server README).

When the gateway has choosen the right microservice to send the request, it starts a synchronous communication and wait for a response, when this one is received then is sent back to the user.

Image above shows how the architecture is built, arrows from the api gateway to the microservices are missing since if they were present, image would be very messy but as I said above, gateway to microservices communication is handled by a synchronous stream.

### Microservices
As shown above, there are several microservices used on our application, the granularity used for splitting them was chosen by considering the resources each microservice would have operated with, so microservices implemented are:

- _assignment_: microservice used to add and remove an assignment;
- _channel_: microservice used to get, add and remove a channel;
- _course_: microservice used to get, add and remove a course;
- _exercise_: microservice used to get, create and answer to an exercise;
- _file_: microservice used to add and remove a file inside a course;
- _filesystem_: special microservice used as storing point for other microservices, this is the only microservice the api gateway doesn't communicate with but other microsevices directly do it in order to create/remove folders or upload/remove files;
- _loginreg_: microservice used to registrate or login a user;
- _message_; microservice used to get or send messages; 
- _result_: microservice used to get assignments results;
- _solution_: microservice used to get or add a solution to an exercise; 
- _subscription_: microservice used to get or add a subscription to a channel or course;
- _test_: microservice used to get or add tests related to an exercise;
- _user_: microservice used to get user information;

Each microservice except filesystem has its own database that is built in order to be independent from other microservices so it has only the necessary to properly work, this allow microservices to operate only on their databases (like microservice architecture asks).

Obviously, this approach requires a data consistency between microservices databases and this is achieved through **RabbitMQ**.

Other than databases, each microservice contains an API interface that allows external entities to use it and also it contains a persistence level developed using _SQLAlchemy_ library (see Task 3 for more information about it).

![Alt Image text](/Task%204/img/microservice.png "Microservice structure")

Above an illustration of a generic microservice.

### RabbitMQ
Each time an INSERT, UPDATE or DELETE query is made by a microservice, this one doesnt' directly communicate with the database but instead it sends a message to an exchanger that insert it into a queue handled by a RabbitMQ server, so we can see each microservice as a **producer** of the message. 

When messaage is queued, a **consumer** of the message will handle it, it reads the content and it performs the operation required inside multiple databases. Therefore each microservice knows only about its database but if a critical operation such as an insertion, an update or a delete inside the database is requested, it will let the consumer perform it without knowing which are the other databases interested on the operation.

![Alt Image text](/Task%204/img/rabbit.png "Representation of the architecture chosen with RabbitMQ")

Thanks to this technology data consistency is now achieved and at the same time microservice architecture philosophy is maintained. 
Above is shown an example image of a microservice sending a critical request to the queue and a consumer handling it by performing the request inside multiple databases.

Notice that in our case we have just one consumer but RabbitMQ is so powerful that we can easily scale it by adding many of them so to improve performances of the system.

### Databases

As said many times before, each microservice has its own independent database, below there is a list of all schema for each microservice database, notice that as for Task 3 _MariaDB_ DBMS is used.

#### Assignment 
![Alt Image text](/Task%204/img/assignment.png "Assignment schema")
#### Channel
![Alt Image text](/Task%204/img/channel.png "Channel schema")
#### Course
![Alt Image text](/Task%204/img/course.png "Course schema")
#### Exercise
![Alt Image text](/Task%204/img/exercise.png "Exercise schema")
#### File
![Alt Image text](/Task%204/img/file.png "File schema")
#### Login
![Alt Image text](/Task%204/img/user.png "Login schema")
#### Message
![Alt Image text](/Task%204/img/message.png "Message schema")
#### Result
![Alt Image text](/Task%204/img/result.png "Result schema")
#### Solution
![Alt Image text](/Task%204/img/solution.png "Solution schema")
#### Subscription
![Alt Image text](/Task%204/img/subscription.png "Subscription schema")
#### Test
![Alt Image text](/Task%204/img/test.png "Test schema")
#### User 
![Alt Image text](/Task%204/img/user.png "User schema")

## How to run the project

In order to build this system there are 2 requirements:
- Docker
- Compose

If you have an updated version of Docker/Docker Desktop, Compose was installed with it.

First of all you have to clone this repo with:
```
$> git clone https://github.com/BrunoFrancesco97/Software_Architectures.git
```
Or you can simply use GitHub Desktop, open a terminal and cd in the root folder of this task.

You can build the system with this command:

```
$> docker-compose build
```

It will create these docker images:
```
$> docker image 
REPOSITORY                             TAG
hackerrank/db_file                   latest
hackerrank/db_user                   latest
hackerrank/db_channel                latest
hackerrank/db_course                 latest
hackerrank/db_message                latest
hackerrank/db_result                 latest
hackerrank/db_solution               latest
hackerrank/db_assignment             latest
hackerrank/db_exercise               latest
hackerrank/db_test                   latest
hackerrank/db_login                  latest
hackerrank/db_subscription           latest
hackerrank/api_exercise              latest
hackerrank/rabbit_consumer           latest
hackerrank/api_wrapper               latest
hackerrank/api_exercise              latest
hackerrank/api_assignment            latest
hackerrank/api_message               latest
hackerrank/api_file                  latest
hackerrank/api_test                  latest
hackerrank/api_result                latest
hackerrank/api_channel               latest
hackerrank/api_course                latest
hackerrank/api_user                  latest
hackerrank/api_login                 latest
hackerrank/api_subscription          latest
hackerrank/api_solution              latest
hackerrank/api_filesystem            latest
hackerrank/app-web                   latest
```

Now you can start the system with:
```
$> docker-compose up
```
Wait until all containers are properly started and enjoy the project by searching _localhost:8080_ on your browser
## Test it
Not all functionalities of the application are implemented or they are implemented partially (example, backend is implemented but not the frontend one), therefore the final artefact presented is just a demo of what a hackerrank like application should be.

In order to ose the application, after having started every container following the guide above, search for _localhost:8080_ on your browser, at this point you should see the login page (below one).

![Alt Image text](/Task%204/img/loginpage.png "Login page")

Before logging into the application, create a new account (user role if you want to check code compilation functionalities), then log in using the new information chosen. First thing you can see is a list of possible channels (here there is only a default one), by clicking on it you can subsribe to the channel (image below).

![Alt Image text](/Task%204/img/subscribe.png "Subscribe modal")

After being subscribed to the channel, click another time on it, you are now entered to the channel and you should see a list of courses related to the channel you entered (currently only a default course), same as channels by clicking on the single course you can subscribe and enter on it.

Now you are entered inside the course, you can check all contents related to this one such as files uploaded by admins or assignments given (image below).

<img src="/Task%204/img/materials.png" width="400">

As you can see there is a default assignment proposed, by clicking on it you enter on a solving page where there is a exercise that need to be solved (image below)
<p align="center">
  <img src="/Task%204/img/exercises.png" width="400">
</p>

## Future improvements
In order to improve the demo proposed, some improvements are shown below:
- Integration of missing features proposed in the previous tasks
- Better graphic interface 
- Better responsive interface
- Better user experience when an exercise is solved 
- Better user experience when a result of an assignment is sent back to the user from the server

# Task 4 Documentation

## Requirements
For this task is asked to build up an Hackerrank-like application over a distributed architecture, Task 3 monolithic application is used as starting point.

## Overview of the architecture used

Since requirements ask for a distributed architecture, the original Task 3 application is now splitted into different services that can be placed inside different communicating machines (in order to simplify life professor, we build a simulation of a distributed architecture so a unique docker compose is used as final artifact), in detail our application is based on *microservices*.

<p align="center">
  <img src="img/global_arch.png">
</p>

## Frontend
The frontend (or presentation level) is composed by two elements:
- Web Server (serve the web app)
- Web App (runs on a browser)

#### Web Server
The web server we use is a minimal Nginx Alpine based dockerized.
Starting from the `nginx:alpine` image we simply insert our web app code in Nginx's html folder.
```
FROM nginx:alpine
COPY <our src directory> /usr/share/nginx/html
```
It is fast and very light-weighted.
The only think this web server have to do is to serve the web app files to a browser.
It's a fully scalable and distributable component.

#### Web App
We developed two different demo app.
- User's app
- Staff's app

We choose (after a Flutter attempt) to make two simple web apps, based on simple frameworks:
- Javascript & jQuery (dom manipulation)
- Bootstrap (css graphics)
- Toastr (fancy ui toasts)
- some other external css stylesheets

The advantage of this presentation level "isolation" is that none server is processing some data to produce final user's ui. The web app process data directly in the browser, using user's computational resources. This can help to provide a good service (see below some network usare hint) but also make cheaper the serverside costs.

## Backend
<p align="center">
  <img src="/Task%204/img/distributed.png">
</p>

#### API Layer 
API layer is the first component met by a user inside backend and is very important since is a proxy to the right microservice but also it handles the login/logout services through JWT cookie (see _Task 3/backend/server/_ for a better explaination of this technology).

A user can send requests to the API layer thanks to a list of fixed endpoints that are the same as task 3 ones so for space reasons they are omitted from being displayed here (see _Task 3/backend/server/_ README).

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

<p align="center">
  <img src="/Task%204/img/microservice.png">
</p>

Above an illustration of a generic microservice.

### RabbitMQ
Each time an INSERT, UPDATE or DELETE query is made by a microservice, this one doesnt' directly communicate with the database but instead it sends a message to an exchanger that insert it into a queue handled by a RabbitMQ server, so we can see each microservice as a **producer** of the message. 

When messaage is queued, a **consumer** of the message will handle it, it reads the content and it performs the operation required inside multiple databases. Therefore each microservice knows only about its database but if a critical operation such as an insertion, an update or a delete inside the database is requested, it will let the consumer perform it without knowing which are the other databases interested on the operation.

<p align="center">
  <img src="/Task%204/img/rabbit.png">
</p>

Thanks to this technology data consistency is now achieved and at the same time microservice architecture philosophy is maintained. 
Above is shown an example image of a microservice sending a critical request to the queue and a consumer handling it by performing the request inside multiple databases.

Notice that in our case we have just one consumer but RabbitMQ is so powerful that we can easily scale it by adding many of them so to improve performances of the system.

### Databases

As said many times before, each microservice has its own independent database, below there is a list of all schema for each microservice database, notice that as for Task 3 _MariaDB_ DBMS is used.

#### Assignment 
<p align="center">
  <img src="/Task%204/img/assignment.png" width="600">
</p>

#### Channel
<p align="center">
  <img src="/Task%204/img/channel.png" width="600">
</p>

#### Course
<p align="center">
  <img src="/Task%204/img/course.png" width="600">
</p>

#### Exercise
<p align="center">
  <img src="/Task%204/img/exercise.png" width="600">
</p>

#### File
<p align="center">
  <img src="/Task%204/img/file.png" width="600">
</p>

#### Login
<p align="center">
  <img src="/Task%204/img/user.png">
</p>

#### Message
<p align="center">
  <img src="/Task%204/img/message.png">
</p>

#### Result
<p align="center">
  <img src="/Task%204/img/result.png">
</p>

#### Solution
<p align="center">
  <img src="/Task%204/img/solution.png" width="600">
</p>

#### Subscription
<p align="center">
  <img src="/Task%204/img/subscription.png" width="600">
</p>

#### Test
<p align="center">
  <img src="/Task%204/img/test.png">
</p>

#### User 
<p align="center">
  <img src="/Task%204/img/user.png">
</p>

## How do we deploy the system
We choose to use `docker compose` to deploy the system.
Because of every microservice is "fully independent" from each other we can deploy them as single Docker images. For every microservices we have a Dockerfile where is defined how the image will be build by Docker build.
Above you can find the two-lines Dockerfile used ti build the Web App image.

An other interesting Dockerfile could be the one used to build the API Wrapper (or API Gateway) image:
```
FROM python:3.9-slim-bullseye

WORKDIR "/home/"

ENV DB_URL=localhost
ENV DB_PORT=3306
ENV DB_NAME=sa
ENV DB_USER=root
ENV DB_PASSWORD=root

COPY ./requirements.txt /home/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

RUN mkdir api
ADD src /home/api

ENTRYPOINT ["python3","api/app.py"]
#ENTRYPOINT ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000
```
Here, starting from an official Debian based Python image it add our source code, it install Python packages dependencies and it set up the entrypoint command (a command launched in the container after it starts).

You can also notice some `ENV` statement. They are environment variables, that live in the container's os environment. These environment variables values are defaults one, you can overwrite them when you create a container based on this image simply specifying them in `docker run -e MY_ENV_VAR='value' <..>` or in your `docker-compose.yaml` .

In order to build and deploy theese microservices we have to build every Dockerfile and we have to define a way to create a container for every builded image.. So we use Docker Compose to achieve this with a couple of command!

Our docker-compose.yaml file describe where Dockerfile is and how we want to create every container.

We also defined some simple startup/shutdown dependencies from all the containers:
- microservices databases do not have any dependencies
- microservices depend on them database and RabbitMQ consumer
- api wrapper (or api gateway) depends on every microservice
- web servier depends on api wrapper (because could be usefull have the frontend online only if the backend is already ready)

Docker Compose automatically manages for us startp and shutdown containers's dependencies.

An example of the login microservice contaienr definition in docker-compose.yaml file:
```
  api_login:
    image: hackerrank/api_login:latest
    build: backend/server/microservices/loginreg
    container_name: api_login
    restart: always
    environment:
      - DB_URL=db_login
      - DB_PORT=3306
      - DB_NAME=sa
      - DB_USER=test
      - DB_PASSWORD=test
      - URL_RABBIT=rabbitmq
    depends_on:
      - db_login
      - rabbit_consumer
```
The first line define the service name "api_login".

The third line define the path of the folder with Dockerfile in it. So using `docker compose build` it know where to search for build declarations.

We setted up a restart policy because we want this container try to restart if Docker detect it crashed.

We also declare some environment variable, and we all know this is not safe to store in a code repo but could be safer user a secret manager.. But this is an other story.

And finally we declare on what other service name this container depends on.

In conclusion, we can affirm that our system probably can be deployed in some orchestrator like Kubernetes without too much problems, maybe in the future! For this task we use Docker Compose because we are more skilled on it.

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

Enter on Task 4 folder and you should see a _docker-compose.yaml_ file, you can now build the system with this command by using terminal:

```
$> docker compose build
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
$> docker compose up
```
Wait until all containers are properly started and enjoy the project by searching _localhost:8080_ on your browser

You can also use:
```
$> docker compose up -d
```
and
```
$> docker compose down
```
To start and stop the containers in detached mode.

## Test it
Not all functionalities of the application are implemented or they are implemented partially (example, backend is implemented but not the frontend one), therefore the final artefact presented is just a demo of what a hackerrank like application should be.

In order to use the application, after having started every container following the guide above, search for _localhost:8080_ on your browser, at this point you should see the login page (below one).

<p align="center">
  <img src="/Task%204/img/loginpage2.png" width="400">
</p>

Before logging into the application, create a new account (user role if you want to check code compilation functionalities), then log in using the new information chosen. First thing you can see is a list of possible channels (here there is only a default one), by clicking on it you can subsribe to the channel (image below).

<p align="center">
  <img src="/Task%204/img/subscribe.png" width="400">
</p>

After being subscribed to the channel, click another time on it, you are now entered to the channel and you should see a list of courses related to the channel you entered (currently only a default course), same as channels by clicking on the single course you can subscribe and enter on it.

Now you are entered inside the course, you can check all contents related to this one such as files uploaded by admins or assignments given (image below).

<p align="center">
  <img src="/Task%204/img/materials.png" width="400">
</p>

As you can see there is a default assignment proposed, by clicking on it you enter on a solving page where there is a exercise that need to be solved (image below)
<p align="center">
  <img src="/Task%204/img/exercises.png" width="400">
</p>

Now you can complete the exercise, some files are already written and they are in _tests_ folder in the main root of this task. When a file is given and solution is calculated, a result page will be showed. By returning in the previous page you can now see the assignment done under the list called "Assignments Done", if you click on it you can see the results obtained of that assignment.

If you wander to have a basic administration experience, you can test our Staff one-page web app. This web app is a simple html/js/css page, served to a browser by a static web server. It completely runs over the browser! Frontend app to backend communications are through http requests to the API gateway/wrapper, so the web server is not involved.

In order to login you must to register an account with "staff" role.
<p align="center">
  <img src="img/staff_login.png" width="400">
</p>

Once logged in, you can see an homepage that in the future could be a synthetic realtime system status report.
<p align="center">
  <img src="img/staff_homepage.png" width="600">
</p>

From the left bar you can manage channels and courses. Currently you can only add or remove theese two type of resources. More work (and a frontend team!) is required in order to develope all the features.
<p align="center">
  <img src="img/staff_addCourse.png" width="600">
</p>

You can see below an example of api calls from the staff web app. As you can see (assuming the web app is cached in browser), the network traffic is very low in order to operate. Withous using "traditional" dinamic web page (serverside generated pages using flask + jinja, ecc) you don't have to scale web server according to users increase, because the web server only have to serve the web app once. Once the browser get the web app, it will communicate directly to the API server(s).
Please, note that the traffic for a single api call is below 1kB, and for example if you have to transfer the full homepage (assuming JS and css already cached) from a server to a browser the network traffic will be above 21kB.
<p align="center">
  <img src="img/staff_httpCalls.png" width="800">
</p>

## Future improvements
In order to improve the demo proposed, some improvements are shown below:
- Integration of missing features proposed in the previous tasks
- Better graphic interface (position and colours of some components, more moden design) 
- Better responsive interface
- Better user experience when an exercise is solved 
- Better user experience when a result of an assignment is sent back to the user from the server
- Deploy over an orchestrator

# Task 3 Documentation

## Requirements and approach
For this task is asked to build up an Hackerrank-like application over a monolithic architecture, thus all parts that form the application are stored inside the same machine.
In order to solve the task we have developed a classical frontend/backend layered application since this approach fits well for our needs. 

In particular our frontend is a Javascript application, meanwhile our backend is divided into three parts:
- the RestAPI server is made by using Flask, an efficient Python framework that allows to build web services
- A persistence layer built using SQLAlchemy
- A database built using MariaDB RDBMS

Acturally we build the system as three Docker image, and we deploy these image inthree different containers.

As you can see, our backend is isolated in Docker envronment.
The frontend is served by and nginx server, runs directly in browser, and send requests to the api server:

![Alt Image text](/Task%203/img/architecture.svg?raw=true "Backend structure")

## Frontend
Frontend is a simple Javascript app, served by an nginx service.
This app run directly in browser, and work as a presentation level.

## Backend
Backend is composed from 3 different layers, they are:
- _APIRest_ layer
- _Persistence_ layer
- _Database_ layer

These layers must interact with each other in order to have a working application and at the same time they can be seen as independent layers but since APIRest and persistence layers are both coded using Python inside the same project, then they are both grouped in _Software_Architectures/Task 3/backend/server/_ folder and also are located in the same Docker image, meanwhile database has an own folder, all its information is stored inside _Software_Architectures/Task 3/backend/db/_ and has also an own Docker image.

![Alt Image text](/Task%203/img/backend.png?raw=true "Backend structure")

Above is shown an image where is summarized how backend is structured.

This division of layers allows the program to scale services if needed in an efficient way and also to allow the distribution of the application. For example if there is an high load of requestes to the RestAPI server, the original container can be duplicated so to help at lowering the load of work independently from the database.

### Backend Documentation
Backend documentation can be found inside each respective folder on _main_ branch, so:
- _Software_Architectures/Task 3/backend/server/_ contains a README that explains how to build and run the single image used to run the APIRest server but also it analyzes each endpoint implemented, how login was secured and a small description about SQLAlchemy, a library that allows the persistence of data between the API and the DB;
- _Software_Architectures/Task 3/backend/db/_ contains a README that explains how to build and run the single image used to run the DBMS used but also it contains a small description of the structure of our database.

## Build guide 
In order to build this system there are 2 requirements:
- Docker
- Compose

If you have an updated version of Docker/Docker Desktop, Compose was installed with it.

First of all you have to clone this repo with:
```
$> git clone git@github.com:BrunoFrancesco97/Software_Architectures.git
```
Or you can simply use GitHub Desktop, open a terminal and cd in the root folder of this project.

Now cd in the

You can build the system with this command:

```
$> docker compose build
```

It will create these three docker images:
```
$> docker image ls
REPOSITORY              TAG
hackerrank/api          latest
hackerrank/db           latest
hackerrank/app-web      latest
```

Now you can start the system with:
```
$> docker compose build
```

According to docker-compose declaration, there are only two exposed endpoints:
- [api server](http://localhost:5000) - port 5000
- [web app](http://localhost:8080) - port 8080
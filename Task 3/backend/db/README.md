
# HackerRank Database
Hackerrank database implemented using MariaDB RDBMS, all deployed inside a Docker image.

## Goals
In order to have a scalable and efficient application, a Docker image with only database service is built up.

This choice of not integrating the database inside the server api image is thus caused by the fact that if the application must handle an heavy load of queries, containers could be duplicated and easily managed through a service like Kubernetees or similar.


## Small description of the database
Database is formed by many tables where each one has its own characteristics.

In order not to be too long-winded, an image representation of the schema implemented is shown below.

![Alt Image text](/Task%203/backend/db/img/db.png?raw=true "Optional Title")

## How to individually run it

If you want use this image inside an independent container, there are two options:
- Pulling it from Docker Hub
- Build the image from the given Dockerfile

First option can be easily done by executing this command on your machine:
```
docker pull francescobruno97/db:latest
```
This allows Docker (previously installed on your device) to download the image from the hub, you can then execute it with this other command:
```
docker run --name <container-name> -p 5000:5000 francescobruno97/db:latest
```

Second option can be done by executing this other commands.

First of all, you need to be inside the same folder of the database Dockerfile, then you run:
```
docker build --no-cache -t <image-name> .
```
After the image is built, you also run:
```
docker run --name <container-name> -p 5000:5000 <image-name>
```
After one of these 2 options, you will have a container with an HackerRank database running on it.


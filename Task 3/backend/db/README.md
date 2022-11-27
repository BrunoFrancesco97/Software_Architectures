
# HackerRank Database
Hackerrank database implemented using MariaDB RDBMS, all deployed inside a Docker image.

## Goals
In order to have a scalable and efficient application, a Docker image with only database service is built up.

This choice of not integrating the database inside the server api image is thus caused by the fact that if the application must handle an heavy load of queries, containers could be duplicated and easily managed through a service like Kubernetees.


## Small description of the database
Database is formed by many tables where each one has its own characteristics.

In order not to be too long-winded, an image representation of the schema implemented is shown below.

![Alt Image text](/Task%203/backend/db/img/db.png?raw=true "Optional Title")

## How to use it

If you want use this image, there are two options:
- Pulling it from Docker Hub
- Build the image from the given Dockerfile

First option can be easily done by executing this command on your machine:
```
docker pull francescobruno97/db:latest
```

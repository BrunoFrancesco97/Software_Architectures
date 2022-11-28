#!/bin/bash
#cd ../app
echo "Let's start building Flutter app Docker image.."
docker build --rm --tag hackerrank/app-web:latest ../app/
echo "Cleaning up.."
docker image prune --filter label=stage=builder
#cd ../backend/db
docker build --rm --tag hackerrank/db:latest ../backend/db
docker build --rm --tag hackerrank/api-server:latest ../backend/server

::This batch script deploy the builded system images using a docker-compose!
@echo off
echo deploy..
docker compose up
::echo %cd%
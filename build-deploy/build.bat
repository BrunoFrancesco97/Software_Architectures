::This batch script build all the system components images: api server, db with pre-filled tables, Flutter app
@echo off
cd ..\app
echo Let's start building Flutter app Docker image..
docker build --rm --tag hackerrank.qg/hackerrank:latest ../app/
docker image prune --filter label=stage=builder

::TODO: remake below control block.. actually it's shieeet
if errorlevel 0 goto ok
echo Something wen wrong.. Exiting!

:ok
echo Success!
echo Builded image: hackerrank.qg/hackerrank:latest
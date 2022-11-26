FROM ubuntu:latest
WORKDIR "/home/"
RUN apt-get update 
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
RUN apt-get install default-jre -y
RUN pip3 install flask
RUN pip3 install flask_jwt_extended
RUN pip3 install pymysql
RUN pip3 install sqlalchemy
RUN mkdir api
ADD api /home/api
ENTRYPOINT ["python3","api/app.py"]

EXPOSE 5000

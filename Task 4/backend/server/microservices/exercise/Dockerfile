# syntax=docker/dockerfile:1
FROM ubuntu:latest

WORKDIR /home

RUN apt-get update
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
RUN apt-get install default-jre -y

ENV DB_URL=db_channel
ENV DB_PORT=3306
ENV DB_NAME=sa
ENV DB_USER=root
ENV DB_PASSWORD=root

COPY ./requirements.txt /home/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

#RUN mkdir assignment
ADD . /home

ENTRYPOINT ["python3","app.py"]
#ENTRYPOINT ["python3","assignment/app.py"]
#ENTRYPOINT ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5008
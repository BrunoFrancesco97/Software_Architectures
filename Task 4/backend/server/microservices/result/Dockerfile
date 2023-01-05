# syntax=docker/dockerfile:1

FROM python:3.9-slim-bullseye

WORKDIR /python-docker

ENV DB_URL=db_channel
ENV DB_PORT=3306
ENV DB_NAME=sa
ENV DB_USER=root
ENV DB_PASSWORD=root

COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

#RUN mkdir assignment
ADD . /python-docker

ENTRYPOINT ["python3","app.py"]
#ENTRYPOINT ["python3","assignment/app.py"]
#ENTRYPOINT ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5010
# syntax=docker/dockerfile:1

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

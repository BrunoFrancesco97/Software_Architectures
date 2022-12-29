FROM ubuntu:latest
WORKDIR "/home/"
ENV DB_URL=localhost
ENV DB_PORT=3306
ENV DB_NAME=sa
ENV DB_USER=root
ENV DB_PASSWORD=root
RUN apt-get update
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
RUN apt-get install default-jre -y
COPY ./requirements.txt /home/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt
#RUN pip3 install flask
#RUN pip3 install flask_jwt_extended
#RUN pip3 install pymysql
#RUN pip3 install sqlalchemy
RUN mkdir api
ADD api /home/api
ENTRYPOINT ["python3","api/app.py"]
#ENTRYPOINT ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "5000"]

EXPOSE 5000

FROM mariadb:latest

RUN apt-get update
ENV MARIADB_USER=test
ENV MARIADB_PASSWORD=test 
ENV MARIADB_DATABASE=sa
ENV MARIADB_ROOT_PASSWORD=root
ADD sa_backup.sql /docker-entrypoint-initdb.d

EXPOSE 3306
CMD ["mysqld"]



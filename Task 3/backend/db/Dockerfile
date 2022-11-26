FROM mariadb:10.5

RUN apt-get update
ENV MARIADB_ROOT_PASSWORD=root 
ENV MARIADB_DATABASE=sa
ADD sa_backup.sql /docker-entrypoint-initdb.d

EXPOSE 3306
CMD ["mysqld"]



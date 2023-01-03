FROM mariadb:latest

RUN apt-get update
ENV MARIADB_USER=test
ENV MARIADB_PASSWORD=test 
ENV MARIADB_DATABASE=assignment
ENV MARIADB_ROOT_PASSWORD=root
ADD 4_test.sql /docker-entrypoint-initdb.d

EXPOSE 3306
CMD ["mysqld"]
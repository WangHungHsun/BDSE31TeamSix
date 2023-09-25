FROM mysql/mysql-server
ENV MYSQL_ROOT_PASSWORD bigred
RUN microdnf update && microdnf install sudo curl wget zip tree iputils hostname findutils procps less nano net-tools && \
microdnf clean all && echo 'local_infile=ON' >> /etc/my.cnf
ADD my.sql /docker-entrypoint-initdb.d
EXPOSE 3306


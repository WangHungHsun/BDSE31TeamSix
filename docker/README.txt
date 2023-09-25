#除了autoGetUrl目錄以外

#每一個目錄區代表一個container

#以下如果有出現
#Docker build的話請在各個container區取得Dockerfile

-----------------------------------------------------

★Flask (去Flask目錄區尋找Dockerfile)


###我們組的相依檔是放在
###bigred@a2:~/wei/front_end0919

1.cd 您存Dockerfile得路徑

2.docker build -t flask_v12_0919 .

3.docker run -d --name flask --restart=always -p 8080:8080 flask_v12_0919

-----------------------------------------------------

★Ngrok

yourtoken:要改成自己的，172.22.34.127:8080:則為flask的port

1.docker run --net=host -e NGROK_AUTHTOKEN=yourtoken -d --restart=always --name ngrok ngrok/ngrok:latest http 172.22.34.127:8080

-----------------------------------------------------

★MySQL

0.如果需要MySQL的那些原檔
  請將MySQL的mydb移到您所使用的家目錄

1.mkdir -p ~/wulin/mysql

2.nano ~/wulin/mysql/Dockerfile

######
FROM mysql/mysql-server
ENV MYSQL_ROOT_PASSWORD bigred
RUN microdnf update && microdnf install sudo curl wget zip tree iputils hostname findutils procps less nano net-tools && \
microdnf clean all && echo 'local_infile=ON' >> /etc/my.cnf
ADD my.sql /docker-entrypoint-initdb.d
EXPOSE 3306
#####

3.nano ~/wulin/mysql/my.sql
#####
REATE USER 'bigred'@'%' IDENTIFIED BY 'bigred';
ALTER USER 'bigred' IDENTIFIED WITH mysql_native_password BY 'bigred';
GRANT ALL PRIVILEGES ON *.* TO 'bigred'@'%' WITH GRANT OPTION;

CREATE USER 'rbean'@'%' IDENTIFIED BY 'rbean';
ALTER USER 'rbean' IDENTIFIED WITH mysql_native_password BY 'rbean';
GRANT ALL PRIVILEGES ON rbean.* TO 'rbean'@'%' WITH GRANT OPTION;

CREATE DATABASE rbean;

FLUSH PRIVILEGES;
#####

4.docker build -t oracle.mysql ~/wulin/mysql

5.docker run --name mydb -p 3306:3306 -d -v ~/mydb:/var/lib/mysql/ oracle.mysql

-----------------------------------------------------

★JupyterNotebook

1.mkdir -p ~/jupyterworkspace/{3.11,3.9,3.10}

docker pull jupyter/scipy-notebook:python-3.11
docker run -d --name j1 --restart=always -p 8888:8888 -v ~/jupyterworkspace/3.11:/home/jovyan/ jupyter/scipy-notebook:python-3.11

docker pull jupyter/scipy-notebook:python-3.9
docker run -d --name j2 --restart=always -p 8889:8888 -v ~/jupyterworkspace/3.9:/home/jovyan/ jupyter/scipy-notebook:python-3.9

docker pull jupyter/scipy-notebook:python-3.10
docker run -d --name j3 --restart=always -p 8890:8888 -v ~/jupyterworkspace/3.10:/home/jovyan/ jupyter/scipy-notebook:python-3.10

管理員將logs j1,j2,j3 的token存到根目錄就可以跟大家分享了

2.sudo mkdir /jupytertoken;cd /jupytertoken

3.echo 'version=3.11
localhost:8888
token=7511afa70503741dd70d0abbd92e0a22f9a3cd9556202521

########

version=3.9
localhost:8889
token=508dcfe3e9d4c9f3c418a589d5b074e5818e4794009eb867

########

version=3.10
localhost:8890
token=b926d3a70173d17b5e775c655624544a94d48cec3fcd5e87' > jupyternb_token

-----------------------------------------------------


要改Flask
cd ~;mkdir wei/
scp 檔案進去

###bigred@a2:~/wei/front_end0920

1.cd ~/wei/front_end0920

2.nano Dockerfile

3.更改
  CMD ["new_flask_test.py"]

4.將讀檔路徑改為相對路徑

5.docker build -t flask_v4_0920 .

6.docker run -d --name flask --restart=always -p 8080:8080 flask_v4_0920



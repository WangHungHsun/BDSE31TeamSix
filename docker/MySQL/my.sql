CREATE USER 'bigred'@'%' IDENTIFIED BY 'bigred';
ALTER USER 'bigred' IDENTIFIED WITH mysql_native_password BY 'bigred';
GRANT ALL PRIVILEGES ON *.* TO 'bigred'@'%' WITH GRANT OPTION;

CREATE USER 'tiffany'@'%' IDENTIFIED BY 'tiffany';
ALTER USER 'tiffany' IDENTIFIED WITH mysql_native_password BY 'tiffany';
GRANT ALL PRIVILEGES ON tiffany.* TO 'tiffany'@'%' WITH GRANT OPTION;
CREATE DATABASE tiffany;

CREATE USER 'jeffrey'@'%' IDENTIFIED BY 'jeffrey';
ALTER USER 'jeffrey' IDENTIFIED WITH mysql_native_password BY 'jeffrey';
GRANT ALL PRIVILEGES ON jeffrey.* TO 'jeffrey'@'%' WITH GRANT OPTION;
CREATE DATABASE jeffrey;

CREATE USER 'hadoopw2'@'%' IDENTIFIED BY 'hadoopw2';
ALTER USER 'hadoopw2' IDENTIFIED WITH mysql_native_password BY 'hadoopw2';
GRANT ALL PRIVILEGES ON hadoopw2.* TO 'hadoopw2'@'%' WITH GRANT OPTION;
CREATE DATABASE hadoopw2;

CREATE USER 'wayne'@'%' IDENTIFIED BY 'wayne';
ALTER USER 'wayne' IDENTIFIED WITH mysql_native_password BY 'wayne';
GRANT ALL PRIVILEGES ON wayne.* TO 'wayne'@'%' WITH GRANT OPTION;
CREATE DATABASE wayne;

CREATE USER 'frank'@'%' IDENTIFIED BY 'frank';
ALTER USER 'frank' IDENTIFIED WITH mysql_native_password BY 'frank';
GRANT ALL PRIVILEGES ON frank.* TO 'frank'@'%' WITH GRANT OPTION;
CREATE DATABASE frank;

CREATE USER 'alfred'@'%' IDENTIFIED BY 'alfred';
ALTER USER 'alfred' IDENTIFIED WITH mysql_native_password BY 'alfred';
GRANT ALL PRIVILEGES ON alfred.* TO 'alfred'@'%' WITH GRANT OPTION;
CREATE DATABASE alfred;

FLUSH PRIVILEGES;


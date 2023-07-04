## Tutorials


### Build up with docker
#### Mysql with docker
  - start mysql with docker: `docker run -itd --name mysqlnew -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql`
  - enter docker container: `docker exec -it mysqlnew bash -l` 
  - enter database: `mysql -u root -p` password: `123456`
  - ensure we could access db: `show databases;`
  - 
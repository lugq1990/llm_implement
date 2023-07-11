
### `big data platform`

Goodness:
- re-usable platform for developer to efficient etl, no need to write spark code
- support webpage based ELT workflow, with visiable data flow for PM and BA



### Technical detail
1. Init mysql 
```sh
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=1234 -p 3306:3306 -d mysql
docker exec -it mysql-container /bin/bash
mysql -u root -p  
create database spark;
use spark;
create table source (name varchar(255), age varchar(255));
insert into source values ("lu", "30");
insert into source values ("gq", "30");
```

--- JDBC connection string: `jdbc:mysql://localhost:3306/spark`
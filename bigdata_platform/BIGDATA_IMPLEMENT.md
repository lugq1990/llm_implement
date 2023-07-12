
### `big data platform`

Goodness:
- re-usable platform for developer to efficient etl, no need to write spark code
- support webpage based ELT workflow, with visiable data flow for PM and BA


### implement details
- Based on spark to create `source`, `trasform`,`sink`, `utils` class that implement detail logic
- Classes information
  - Source supported: 
    - File
    - JDBC
    - HIVE
    - MongoDB
    - HBase
  - Trasform supported:
    - select
    - join
    - groupby
    - lit
    - drop
    - filter
    - sort
    - union
    - persist
    - repartion
    - sparksql
  - Sink supported:
    - File
    - JDBC
    - HIVE
    - MongoDB
    - HBase
- Based on `networkx` to create DAG with a pipeline from config file, based topologic order to execute, a dict that contain source id and relative DF
- Based on `airflow` to create job scheduling, job monitoring, DAGs is created based on the config parameter
- 


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
2. JDBC connection
--- JDBC connection string: `jdbc:mysql://localhost:3306/spark`
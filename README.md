# Tutorial for docker-container/ Airflow Docker /MySQL integration
### Business Intelligence (UAL 2018)


### Install a Sample Database in MySQL 

```
mysql --host=localhost --user=xxx --password=xxx
```
exit and run

```
mysql -t < employees.sql
```

confirm the employee database creation in MyQSL.
Besides this one, there should be a database called dwh


### Create a docker container and execute tests

Install (git clone) this repo

- https://github.com/nunobbras/airflow_for_bi


### Test your docker installation 

Docker Build

```
-t puckel/docker-airflow
```

Create containers and keep them alive, restart and delete them

```
docker-compose -f docker-compose-SequentialExecutor.yml up -d

docker-compose -f docker-compose-SequentialExecutor.yml restart

docker-compose -f docker-compose-SequentialExecutor.yml down

```


Run and close a container bash (good to interct once with the airflow)

```
docker-compose -f docker-compose-SequentialExecutor.yml run --rm webserver bash
```

Check existent containers

```
docker conatiner ls
```

Run in a specific container bash

```
docker exec -it dockerairflow_webserver_1 bash
```

Test a specific airflow function in docker

```
docker exec -it dockerairflow_webserver_1 airflow list_dags
```


Execute through bash interactively a test (this will actually work!)

```
docker exec -it dockerairflow_webserver_1 bash
cd dags
airflow test init_etl_example first_task 2015-06-01

```

execute remotely the same test

```
docker exec -it dockerairflow_webserver_1 airflow test init_etl_example first_task 2015-06-01
```


### Run a real DAG - configuration - just run Once!

Create a Run manually (it could be done in the DAG webPage)

```
docker exec -it dockerairflow_webserver_1 airflow trigger_dag init_etl_example
```

Now you can see it ready to work to be fired in web server. We now have to run airflow scheduler to run available 

```
docker exec -it dockerairflow_webserver_1 airflow scheduler
```


### Try out the new connections in the webApp

Go to Data Profiling and use Ad Hoc Query. Make a query you know it returns values.

### Run a simple python script with database connection

testing version

```
docker exec -it dockerairflow_webserver_1 airflow test get_salaries extract_salaries 1999-12-30
```

### If needed, files could be changed inside the docker container using

```
docker cp ./airflow/config/airflow.cfg dockerairflow_webserver_1:/usr/local/airflow
```

### Create a DAG to copy new data to the dwh database

Use the dag in file `process_salaries` and don't forget to create a similar table `employees` in dwh database; 

```
docker exec -it dockerairflow_webserver_1 airflow test process_salaries extract_salaries 1999-1-30
```


### Create a DAG to schedule automatic data injection in OLTP 





### Generate sensors to act upon newly arrived data












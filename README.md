# Tutorial for docker-container/ Airflow Docker /MySQL integration
# Business Intelligence (UAL 2018)

----

## Install a Sample Database in MySQL 

Install from database folder

```
mysql --host=localhost --user=xxx --password=xxx
```
exit and run

```
mysql -t < employees.sql
```

confirm the employee database creation in MyQSL.
Besides this one, there should be a database called dwh


## Create a docker container and execute tests

Install (git clone) this repo

- https://github.com/nunobbras/airflow_for_bi


### Test your docker installation 


Create containers building the images at the same time (see Dockerfile) 

```
docker-compose -f docker-compose-SequentialExecutor.yml up -d
```

and manage them (restart and delete them) if needed

```
docker-compose -f docker-compose-SequentialExecutor.yml restart

docker-compose -f docker-compose-SequentialExecutor.yml down

```


Run and close a container bash (good to interact once with the airflow)

```
docker-compose -f docker-compose-SequentialExecutor.yml run --rm webserver bash
```

Check existent containers

```
docker container ls
```

Run in a specific container bash

```
docker exec -it airflow_for_bi_webserver_1 bash
```
> Note: check the name of the generated components: they could be different than `airflow_for_bi_XXX`


Test a specific airflow function in docker

```
docker exec -it airflow_for_bi_webserver_1 airflow list_dags
```


Execute through bash interactively a test (this will actually work!)

```
docker exec -it airflow_for_bi_webserver_1 bash
cd dags
airflow test init_configuration first_task 2015-06-01

```

execute remotely the same test

```
docker exec -it airflow_for_bi_webserver_1 airflow test init_configuration first_task 2015-06-01
```


### Run a real DAG - configuration

Create a Run manually (it could be done in the DAG webPage)
This is the same DAG as before (init_configuration) but now we are running al the tasks, which includes second_task, that makes a airflow configuration (see the code of `init_configuration.py`)

```
docker exec -it airflow_for_bi_webserver_1 airflow trigger_dag init_configuration
```

Now you can see it ready to work to be fired in web server. We now have to run airflow scheduler to run available 

```
docker exec -it airflow_for_bi_webserver_1 airflow scheduler
```


### Try out the new connections in the webApp

Go to Data Profiling and use Ad Hoc Query. Make a query you know it returns values.

### Run a simple python script with database connection

testing version

```
docker exec -it airflow_for_bi_webserver_1 airflow test get_salaries extract_salaries 1999-12-30
```

### If needed, files could be changed inside the docker container using

```
docker cp ./airflow/config/airflow.cfg airflow_for_bi_webserver_1:/usr/local/airflow
```

### Create a DAG to copy new data to the dwh database

Use the dag in file `process_salaries` and don't forget to create a similar table `employees` in dwh database; 

```
docker exec -it airflow_for_bi_webserver_1 airflow test process_salaries extract_salaries 1999-1-30
```


### Create a DAG to schedule automatic data injection in OLTP 





### Generate sensors to act upon newly arrived data












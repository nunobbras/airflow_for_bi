# Tutorial for docker-container/ Airflow Docker /MySQL integration
# Business Intelligence (UAL 2018)

----

## Install a Sample Database in MySQL 

Run from `database` folder:

```
mysql --host=localhost --user=xxx --password=xxx 
```

and in mysql run

```
source employees.sql
```


confirm the employee database creation in MyQSL.

Besides this one, there should be a database called dwh (Run from  `dwh` folder):

```
mysql --host=localhost --user=xxx --password=xxx 
```

and in mysql run

```
source salaries.sql
```



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

Let's use the DAG `inject_salaries` to generate data automatically in salaries table;

For that to work you can start by testing it with 

```
docker exec -it airflow_for_bi_webserver_1 airflow test inject_salaries inject_salaries_operator 2015-01-01
```

This should generate an extra set of 10 rows of salaries for random employees for the month `2015-01`.

You should now be able to start the scheduler and activate this task. Make it work 2 times per day; 
Also, run previous dates (1 year) using airflow backfill, starting at 2017, using 

```
docker exec -it airflow_for_bi_webserver_1 airflow backfill inject_salaries -s 2017-05-01 -e 2018-05-01
```



### Generate a DAG to act upon newly arrived data

Given this we should now import from OLTP to dwh from time to time. For that we have to build a DAG that import data from one place to another. For now we are building a simple scheduled DAG that will push data to the same `dwh`. 

For that you should run twice per day the DAG `process_salaries`. Start by testing it with.

```
docker exec -it airflow_for_bi_webserver_1 airflow test process_salaries process_salaries_operator 1/5/2001
```

You can see now you have new data in the `dwh.salaries` database;


# Starting with SUPERSET

## Installation

#### Run Superset as a docker container

(included in the docker-compose file)

#### You can also Install locally superset

make

```
pip install superset
pip install flask-appbuilder
pip install ipython
pip install mysqlclient
pip install cryptography
```



#### Create an admin user (you will be prompted to set username, first and last name before setting a password)
```
docker exec -it airflow_for_bi_superset_1 superset-init
```

if not using docker container make 

```
fabmanager create-admin --app superset
```



#### Initialize the database
```
superset db upgrade
```

#### Load some data to play with
```
superset load_examples
```

#### Create default roles and permissions
```
superset init
```

To start a development web server on port 8088, use -p to bind to another port

```
superset runserver -d
```



----

#### Explore Superset

Create a connection to `dwh` in Sources > Databases

To connect to your local mysql use in `SQLAlchemy URI` field the following path

```
mysql://[mysqluser]:[mysqlpassword]@host.docker.internal:3306/dwh
```

OK! You can now test the connection and move on
























import airflow
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow import models
from airflow.settings import Session
import logging

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(7),
    'provide_context': True
}


def simple_test():
    logging.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    logging.info('This is just a simple task that prints to the SCREEN')
    logging.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    print("Here it goes... Done")


def generate_config():
    logging.info('Creating connections, pool and sql path')

    session = Session()

    def create_new_conn(session, attributes):
        if Session.query(models.Connection).filter(models.Connection.conn_id == attributes.get("conn_id").count() == 0):
            new_conn = models.Connection()
            new_conn.conn_id = attributes.get("conn_id")
            new_conn.conn_type = attributes.get('conn_type')
            new_conn.host = attributes.get('host')
            new_conn.port = attributes.get('port')
            new_conn.schema = attributes.get('schema')
            new_conn.login = attributes.get('login')
            new_conn.set_password(attributes.get('password'))

            session.add(new_conn)
            session.commit()
        else:
            logging.info('Connection {} already exists'.format(
                attributes.get("conn_id")))

    create_new_conn(session,
                    {"conn_id": "mysql_oltp",
                     "conn_type": "mysql",
                     "host": "host.docker.internal",
                     "port": 3306,
                     "schema": "employees",
                     "login": "root",
                     "password": "nbras"})

    create_new_conn(session,
                    {"conn_id": "mysql_dwh",
                     "conn_type": "mysql",
                     "host": "host.docker.internal",
                     "port": 3306,
                     "schema": "dwh",
                     "login": "root",
                     "password": "nbras"})

    create_new_conn(session,
                    {"conn_id": "postgres_oltp",
                     "conn_type": "postgres",
                     "host": "host.docker.internal",
                     "port": 5432,
                     "schema": "dwh",
                     "login": "root",
                     "password": "nbras"})

    create_new_conn(session,
                    {"conn_id": "postgres_dwh",
                     "conn_type": "postgres",
                     "host": "host.docker.internal",
                     "port": 5432,
                     "schema": "dwh",
                     "login": "root",
                     "password": "nbras"})

    new_var = models.Variable()
    new_var.key = "sql_template_paths"
    new_var.set_val("./sql_templates")
    session.add(new_var)
    session.commit()

    new_pool = models.Pool()
    new_pool.pool = "mysql_dwh"
    new_pool.slots = 10
    new_pool.description = "Allows max. 10 connections to the DWH"

    session.add(new_pool)
    session.commit()

    session.close()


dag = airflow.DAG(
    'init_configuration',
    schedule_interval="@once",
    default_args=args,
    max_active_runs=1)

t1 = PythonOperator(task_id='first_task',
                    python_callable=simple_test,
                    provide_context=False,
                    dag=dag)


t2 = PythonOperator(task_id='second_task',
                    python_callable=generate_config,
                    provide_context=False,
                    dag=dag)


t1 >> t2

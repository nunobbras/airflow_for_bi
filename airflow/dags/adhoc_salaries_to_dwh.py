# # [NBB] Connect and query with a jinja template

# from __future__ import print_function
# from airflow import DAG, utils
# from datetime import datetime, timedelta, date
# from etl.operators.dwh_operators import MysqlInsertOperator, MysqlQueryOperatorWithTemplatedParams
# from airflow.operators.python_operator import PythonOperator
# from airflow.models import Variable
# from airflow.macros import ds_format
# import calendar
# import random


# args = {
#     'owner': 'airflow',
#     'start_date': datetime(1950, 1, 1),
#     'provide_context': True,
#     'depends_on_past': True
# }


# tod = date.today()
# month_limits = [tod.replace(day=1), tod.replace(
#     day=calendar.monthrange(tod.year, tod.month)[1])]

# try:
#     tmpl_search_path = Variable.get("sql_template_paths")

#     dag = DAG(
#         'adhoc_operation',
#         schedule_interval="0 * * * * *",
#         dagrun_timeout=timedelta(minutes=60),
#         template_searchpath=tmpl_search_path,
#         default_args=args,
#         max_active_runs=1
#     )

#     get_employees = MysqlQueryOperatorWithTemplatedParams(
#         task_id='get_employee',
#         mysql_conn_id='mysql_oltp',
#         sql='select_rand_employees.sql',
#         parameters={},
#         dag=dag)

#     prepare_data = PythonOperator(
#         task_id='prepare_data', dag=dag, python_callable=prepare_data)

#     insert_salaries = MysqlInsertOperator(
#         task_id='insert_salaries',
#         mysql_conn_id='mysql_dwh',
#         sql='insert_salaries.sql',

#         dag=dag)

#     get_employees >> prepare_data >> insert_salaries

# except:
#     print("warning: no sql_template_paths yet")
#     tmpl_search_path = ""


# def prepare_data(**kwargs):
#     ti = kwargs['ti']
#     data = ti.xcom_pull(key=None, task_ids='get_employees')
#     print("data", data)
#         parameters = {
#             "salary": random.randint(1, 10000),
#             "from_date": "{{ ds }}",
#             "to_date": "{{ ds }}",
#             "import_data": "{{ ds }}",
#         },


# if __name__ == "__main__":
#     dag.cli()

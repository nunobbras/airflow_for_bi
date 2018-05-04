# [NBB] Connect and query with a jinja template

from __future__ import print_function
from airflow import DAG, utils
from datetime import datetime, timedelta
from etl.operators.dwh_operators import MysqlToMysqlOperator
from airflow.models import Variable
import calendar
import random

args = {
    'owner': 'airflow',
    'start_date': datetime(1950, 1, 1),
    'provide_context': True,
    'depends_on_past': True
}


def get_dates(ds):
    tod = ds
    month_limits = [str(tod.replace(day=1)), str(tod.replace(
        day=calendar.monthrange(tod.year, tod.month)[1]))]
    return month_limits


try:
    tmpl_search_path = Variable.get("sql_template_paths")
except:
    print("warning: no sql_template_paths yet")
    tmpl_search_path = ""

dag = DAG(
    'inject_salaries',
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
    template_searchpath=tmpl_search_path,
    default_args=args,
    max_active_runs=1
)

inject_salaries_operator = MysqlToMysqlOperator(
    sql='select_rand_employees.sql',
    dest_table='salaries',
    src_mysql_conn_id='mysql_oltp',
    dest_mysqls_conn_id='mysql_oltp',
    query_parameters={
        "from_date": get_dates(dag.default_args["start_date"])[0],
        "to_date": get_dates(dag.default_args["start_date"])[1]
    },
    task_id='inject_salaries_operator',
    dag=dag)


if __name__ == "__main__":
    dag.cli()

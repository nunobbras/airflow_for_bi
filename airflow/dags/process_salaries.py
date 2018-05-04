# [NBB] Connect and query with a jinja template

from __future__ import print_function
from airflow import DAG, utils
from datetime import datetime, timedelta
from etl.operators.dwh_operators import MysqlToMysqlOperator
from airflow.models import Variable

args = {
    'owner': 'airflow',
    'start_date': datetime(1950, 1, 1),
    'provide_context': True,
    'depends_on_past': True
}

try:
    tmpl_search_path = Variable.get("sql_template_paths")
    dag = DAG(
        'process_salaries',
        schedule_interval="@daily",
        dagrun_timeout=timedelta(minutes=60),
        template_searchpath=tmpl_search_path,
        default_args=args,
        max_active_runs=1
    )

    process_salaries_operator = MysqlToMysqlOperator(
        sql='select_salaries.sql',
        dest_table='salaries',
        src_mysql_conn_id='mysql_oltp',
        dest_mysqls_conn_id='mysql_dwh',
        mysql_preoperator="DELETE FROM dwh.salaries WHERE from_date >= DATE '{{ ds }}' AND from_date < DATE '{{ tomorrow_ds }}'",
        query_parameters={"window_start_date": "{{ ds }}",
                          "window_end_date": "{{ tomorrow_ds }}"},
        task_id='process_salaries_operator',
        dag=dag,
        pool='mysql_dwh')

except:
    print("warning: no sql_template_paths yet")
    tmpl_search_path = ""


if __name__ == "__main__":
    dag.cli()

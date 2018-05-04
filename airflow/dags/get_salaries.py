# [NBB] Connect and query with a jinja template

from __future__ import print_function
from airflow import DAG, utils
from datetime import datetime, timedelta
from etl.operators.dwh_operators import MysqlQueryOperatorWithTemplatedParams
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
        'get_salaries',
        schedule_interval="@daily",
        dagrun_timeout=timedelta(minutes=60),
        template_searchpath=tmpl_search_path,
        default_args=args,
        max_active_runs=1
    )

    process_salaries_dim = MysqlQueryOperatorWithTemplatedParams(
        task_id='extract_salaries',
        mysql_conn_id='mysql_oltp',
        sql='select_salaries.sql',
        parameters={"window_start_date": "{{ ds }}",
                    "window_end_date": "{{ tomorrow_ds }}"},
        dag=dag)

except:
    print("warning: no sql_template_paths yet")
    tmpl_search_path = ""

if __name__ == "__main__":
    dag.cli()

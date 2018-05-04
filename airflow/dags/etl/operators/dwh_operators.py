# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime


class MysqlToMysqlOperator(BaseOperator):

    template_fields = ('sql', 'query_parameters', 'dest_table',
                       'mysql_preoperator', 'mysql_postoperator')
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self,
            sql,
            dest_table,
            src_mysql_conn_id=None,
            dest_mysqls_conn_id=None,
            mysql_preoperator=None,
            mysql_postoperator=None,
            query_parameters=None,
            *args, **kwargs):
        super(MysqlToMysqlOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.dest_table = dest_table
        self.src_mysql_conn_id = src_mysql_conn_id
        self.dest_mysqls_conn_id = dest_mysqls_conn_id
        self.mysql_preoperator = mysql_preoperator
        self.mysql_postoperator = mysql_postoperator
        self.query_parameters = query_parameters

    def execute(self, context):
        logging.info('Executing: ' + str(self.sql))
        src_mysql = MySqlHook(mysql_conn_id=self.src_mysql_conn_id)
        dest_mysql = MySqlHook(mysql_conn_id=self.dest_mysqls_conn_id)

        logging.info(
            "Transferring Mysql query results into other Mysql database.")
        conn = src_mysql.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql, self.query_parameters)

        if self.mysql_preoperator:
            logging.info("Running Mysql preoperator")
            dest_mysql.run(self.mysql_preoperator)

        if cursor.rowcount != 0:
            logging.info("Inserting rows into Mysql")
            for i, row in enumerate(cursor):
                print("row", row)
            dest_mysql.insert_rows(table=self.dest_table, rows=cursor)
            logging.info(str(cursor.rowcount) + " rows inserted")
        else:
            logging.info("No rows inserted")

        if self.mysql_postoperator:
            logging.info("Running Mysql postoperator")
            dest_mysql.run(self.mysql_postoperator)

        logging.info("Done.")


class MysqlQueryOperatorWithTemplatedParams(BaseOperator):
    template_fields = ('sql', 'parameters')
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self, sql,
            mysql_conn_id='mysql_dwh',
            autocommit=False,
            parameters=None,
            *args, **kwargs):
        super(MysqlQueryOperatorWithTemplatedParams,
              self).__init__(*args, **kwargs)
        self.sql = sql
        self.mysql_conn_id = mysql_conn_id
        self.autocommit = autocommit
        self.parameters = parameters

    def execute(self, context):
        logging.info('Executing: ' + str(self.sql), self.parameters)
        self.hook = MySqlHook(mysql_conn_id=self.mysql_conn_id)
        data = self.hook.get_records(self.sql,
                                     parameters=self.parameters)
        #logging.info('Executed: ' + str(x))
        return data


class MysqlInsertOperator(BaseOperator):
    template_fields = ('data_cursor', 'cursor', 'dest_table', 'dest_mysqls_conn_id',
                       'mysql_preoperator', 'mysql_postoperator')
    template_ext = ('.sql')
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self,
            dest_table,
            data_cursor=None,
            cursor=None,
            dest_mysqls_conn_id=None,
            mysql_postoperator=None,
            mysql_preoperator=None,
            *args, **kwargs):
        super(MysqlInsertOperator,
              self).__init__(*args, **kwargs)
        self.dest_table = dest_table
        self.dest_mysqls_conn_id = dest_mysqls_conn_id
        self.mysql_preoperator = mysql_preoperator
        self.mysql_postoperator = mysql_postoperator
        self.cursor = cursor

    def execute(self, context):
        dest_mysql = MySqlHook(mysql_conn_id=self.dest_mysqls_conn_id)

        self.cursor = self.cursor if not data_cursor else kwargs['ti'].xcom_pull(
            key=None, task_ids=data_cursor)

        logging.info(
            "Transferring cursor into new Mysql database.")

        if self.mysql_preoperator:
            logging.info("Running Mysql preoperator")
            dest_mysql.run(self.mysql_preoperator)

            dest_mysql.insert_rows(table=self.dest_table, rows=self.cursor)
            logging.info(self.cursor.rowcount, " rows inserted")
        else:
            logging.info("No rows inserted")

        if self.mysql_postoperator:
            logging.info("Running Mysql postoperator")
            dest_mysql.run(self.mysql_postoperator)

        logging.info("Done.")

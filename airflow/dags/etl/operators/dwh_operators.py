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
    """
    Executes sql code in a Mysql database and inserts into another

    :param src_mysql_conn_id: reference to the source mysql database
    :type src_mysql_conn_id: string
    :param dest_mysqls_conn_id: reference to the destination mysql database
    :type dest_mysqls_conn_id: string
    :param sql: the sql code to be executed
    :type sql: Can receive a str representing a sql statement,
        a list of str (sql statements), or reference to a template file.
        Template reference are recognized by str ending in '.sql'
    :param parameters: a parameters dict that is substituted at query runtime.
    :type parameters: dict
    """

    template_fields = ('sql', 'parameters', 'dest_table',
                       'mysql_preoperator', 'mysql_postoperator')
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self,
            sql,
            dest_table,
            src_mysql_conn_id='mysql_oltp',
            dest_mysqls_conn_id='mysql_dwh',
            mysql_preoperator=None,
            mysql_postoperator=None,
            parameters=None,
            *args, **kwargs):
        super(MysqlToMysqlOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.dest_table = dest_table
        self.src_mysql_conn_id = src_mysql_conn_id
        self.dest_mysqls_conn_id = dest_mysqls_conn_id
        self.mysql_preoperator = mysql_preoperator
        self.mysql_postoperator = mysql_postoperator
        self.parameters = parameters

    def execute(self, context):
        logging.info('Executing: ' + str(self.sql))
        src_pg = MySqlHook(mysql_conn_id=self.src_mysql_conn_id)
        dest_pg = MySqlHook(mysql_conn_id=self.dest_mysqls_conn_id)

        logging.info(
            "Transferring Mysql query results into other Mysql database.")
        conn = src_pg.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql, self.parameters)

        if self.mysql_preoperator:
            logging.info("Running Mysql preoperator")
            dest_pg.run(self.mysql_preoperator)

        logging.info("Inserting rows into Mysql")

        dest_pg.insert_rows(table=self.dest_table, rows=cursor)

        if self.mysql_postoperator:
            logging.info("Running Mysql postoperator")
            dest_pg.run(self.mysql_postoperator)

        logging.info("Done.")


class MysqlOperatorWithTemplatedParams(BaseOperator):
    """
    Executes sql code in a specific Mysql database

    :param mysql_conn_id: reference to a specific mysql database
    :type mysql_conn_id: string
    :param sql: the sql code to be executed
    :type sql: Can receive a str representing a sql statement,
        a list of str (sql statements), or reference to a template file.
        Template reference are recognized by str ending in '.sql'
    """

    template_fields = ('sql', 'parameters')
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self, sql,
            mysql_conn_id='mysql_dwh', autocommit=False,
            parameters=None,
            *args, **kwargs):
        super(MysqlOperatorWithTemplatedParams,
              self).__init__(*args, **kwargs)
        self.sql = sql
        self.mysql_conn_id = mysql_conn_id
        self.autocommit = autocommit
        self.parameters = parameters

    def execute(self, context):
        logging.info('Executing: ' + str(self.sql), self.parameters)
        self.hook = MySqlHook(mysql_conn_id=self.mysql_conn_id)
        x = self.hook.get_records(self.sql,
                                  parameters=self.parameters)
        logging.info('Executed: ' + str(x))

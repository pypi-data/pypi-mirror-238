import datetime
import logging
import pytz
import warnings
import pandas as pd
from psycopg2 import connect
from ..y4a_credentials import get_credentials

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

warnings.filterwarnings("ignore", category=UserWarning)


class MonitorUserExternal:
    def __init__(
        self,
        conn_username: str,
        conn_password: str,
        conn_host: str,
        conn_db: str,
        conn_number: int,
    ) -> None:
        self.conn_username = conn_username
        self.conn_password = conn_password
        self.conn_host = conn_host
        self.conn_db = conn_db
        self.conn_number = conn_number

        self.log_conn_df = pd.DataFrame(
            {
                'time_conn': str(
                    datetime.datetime.now(
                        pytz.timezone('Asia/Ho_Chi_Minh'),
                    ).replace(microsecond=0).replace(tzinfo=None)
                ),
                'host': self.conn_host,
                'username': self.conn_username,
                'password': self.conn_password,
                'database': self.conn_db,
                'num_conn': self.conn_number,
            },
            index=[0],
        )

    def execute(
        self,
        sql: str,
        vars: tuple = None,
        fetch_output: bool = False,
    ) -> list:
        output = None

        credentials = get_credentials(
            platform='pg',
            account_name='clong',
        )

        conn = connect(
            user=credentials['user_name'],
            password=credentials['password'],
            host='172.30.105.100',
            port=5432,
            database='y4a_datawarehouse',
        )

        try:
            cur = conn.cursor()

            cur.execute(sql, vars)

            if fetch_output:
                output = cur.fetchall()

            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        return output

    def generate_log_conn(self) -> None:
        sql = "INSERT INTO y4a_sop.monitor_user_sql_connection "
        sql += "(time_conn, host, username, database, num_conn) "
        sql += f"VALUES ('{self.log_conn_df['time_conn'].values[0]}', "
        sql += f"'{self.log_conn_df['host'].values[0]}', "
        sql += f"'{self.log_conn_df['username'].values[0]}', "
        sql += f"'{self.log_conn_df['database'].values[0]}', "
        sql += f"{self.log_conn_df['num_conn'].values[0]}) "

        self.execute(
            sql=sql,
            fetch_output=False,
        )

    def generate_log_query(
        self,
        sql_query: str,
        duration_query: float,
        is_successed: int,
    ) -> None:
        sql = "INSERT INTO y4a_sop.monitor_user_sql_query "
        sql += "(time_query, host, username, database, "
        sql += "sql_query, duration, is_successed) "
        sql += f"VALUES ('{self.log_conn_df['time_conn'].values[0]}', "
        sql += f"'{self.log_conn_df['host'].values[0]}', "
        sql += f"'{self.log_conn_df['username'].values[0]}', "
        sql += f"'{self.log_conn_df['database'].values[0]}', "
        sql += "%s, "
        sql += f"{duration_query}, "
        sql += f"{is_successed}) "

        self.execute(
            sql=sql,
            vars=(
                sql_query,
            ),
            fetch_output=False,
        )

    def grant_table(
        self,
        schema: str,
        table: str,
        list_users: list,
        privileges: list = ['SELECT'],
        all_privileges: bool = False,
    ) -> None:
        credentials = get_credentials(
            platform='pg',
            account_name='clong',
        )

        conn = connect(
            user=credentials['user_name'],
            password=credentials['password'],
            host=self.conn_host,
            port=5432,
            database=self.conn_db,
        )

        try:
            cur = conn.cursor()

            if 'da' in list_users:
                list_users = [
                    get_credentials(
                        platform='pg',
                        account_name=user,
                    )['user_name'] for user in [
                        'linhvk', 'giangpt', 'hieulm',
                        'huongtmt', 'pi', 'toannh',
                        'trieuna', 'hieulm', 'hoaidtm',
                        'duikha', 'longgh', 'huypv',
                        'huytln', 'quandm', 'nguyentnt',
                        'clong',
                    ]
                ]
            else:
                list_users = [
                    get_credentials(
                        platform='pg',
                        account_name=user,
                    )['user_name'] for user in list_users
                ]

            for user in list_users:
                schema_grant = f"GRANT USAGE ON SCHEMA {schema} TO {user}"
                cur.execute(schema_grant)
                logging.info(f'Grant schema usage for {user}')

                if all_privileges:
                    table_grant = f"GRANT ALL PRIVILEGES ON {schema}.{table} "
                    table_grant += f"to {user}"
                else:
                    table_privileges = ', '.join(privileges)
                    table_grant = f"GRANT {table_privileges} ON "
                    table_grant += f"{schema}.{table} to {user}"

                cur.execute(table_grant)
                logging.info(table_grant)

            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

import logging
import warnings
from ..gg_api.y4a_sheet import GGSheetUtils
from ..datalake.y4a_minio import MinioUtils
from ..sql.y4a_postgresql import PostgreSQLUtils
from ..sql.y4a_mysql import MySQLUtils

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

warnings.filterwarnings("ignore", category=UserWarning)


class DAConfig:
    def __init__(
        self,
        account_name: str,
        **kwargs,
    ) -> None:
        # Google Sheet utils
        self.sheet_utils = GGSheetUtils(
            account_name='da',
        )

        # MinIO utils
        self.minio_utils = MinioUtils(
            account_name='sop',
        )

        # PostgreSQL utils
        self.pg_raw_r_utils = PostgreSQLUtils(
            account_name=account_name,
            pg_name='raw_repl',
        )
        self.pg_raw_w_utils = PostgreSQLUtils(
            account_name=account_name,
            pg_name='raw_master',
        )
        self.pg_serving_r_utils = PostgreSQLUtils(
            account_name=account_name,
            pg_name='serving_repl',
        )
        self.pg_serving_w_utils = PostgreSQLUtils(
            account_name=account_name,
            pg_name='serving_master',
        )

        # MySQL utils
        self.mysql_utils = MySQLUtils(
            account_name='da',
        )

        for key, value in kwargs.items():
            setattr(self, key, value)

import requests
import logging
import warnings
from io import BytesIO
from minio import Minio
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def get_credentials(
    platform: str,
    account_name: str,
) -> None:
    try:
        response = requests.get(
            f'http://172.30.15.171:5431/v1/users/credentials'
            f'/{platform}/{account_name}'
        ).json()
    except Exception as e:
        logging.error(e)
        client = Minio(
            endpoint='storage-api.yes4all.internal',
            access_key='sc_EfcXbWfLekra8O1s',
            secret_key='FbBUuCDliEdgiHDUluBy8q2TBIXlWLak',
            secure=False,
        )
        parquet_data = BytesIO(
            client.get_object(
                bucket_name='sc-bucket',
                object_name='prod/creds.parquet',
            ).data
        )
        df = pd.read_parquet(parquet_data)

        response = df.loc[
            (df['platform'] == platform)
            & (df['account_name'] == account_name)
        ]['values'].values[0]

    return response

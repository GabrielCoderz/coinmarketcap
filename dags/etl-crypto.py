from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
import uuid
import json
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
path_temp_csv = "/tmp/dataset.csv"

dag = DAG(
    dag_id="etl-pipeline-coin-market-cap",
    description="Pipeline para o processo de ETL dos ambientes de produção oltp ao olap.",
    start_date=days_ago(2),
    schedule_interval=None,
)

def _extract():
    parameters = {
        'start':'1',
        'limit':'500',
        'convert':'USD'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    id = []
    name = []
    symbol = []
    data_added = []
    last_updated = []
    price = []
    volume_24h = []
    circulating_supply = []
    total_supply = []
    max_supply = []
    volume_24h = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []

    try:
        response = session.get(api_url, params=parameters)
        data = json.loads(response.text)
        
        for coin in data['data']:
            id.append(uuid.uuid4())
            name.append(coin['name'])
            symbol.append(coin['symbol'])
            data_added.append(coin['date_added'])
            last_updated.append(coin['last_updated'])
            circulating_supply.append(coin['circulating_supply'])
            total_supply.append(coin['total_supply'])
            max_supply.append(coin['max_supply'])
            price.append(coin['quote']['USD']['price'])
            volume_24h.append(coin['quote']['USD']['volume_24h'])
            percent_change_1h.append(coin['quote']['USD']['percent_change_1h'])
            percent_change_24h.append(coin['quote']['USD']['percent_change_24h'])
            percent_change_7d.append(coin['quote']['USD']['percent_change_7d'])

        coin_dict = {
            "id": id,
            "name" : name,
            "symbol": symbol,
            "data_added" : data_added,
            "last_updated" : last_updated,
            "price": price,
            "volume_24h": volume_24h,
            "circulating_supply" : circulating_supply,
            "total_supply": total_supply,
            "max_supply": max_supply,
            "percent_change_1h": percent_change_1h,
            "percent_change_24h": percent_change_24h,
            "percent_change_7d": percent_change_7d
        }

        coins_df = pd.DataFrame(coin_dict)

        coins_df.to_csv(path_temp_csv, index=False)
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)    

def _transform():
    dataset_df = pd.read_csv(path_temp_csv)

    dataset_df["price"] = dataset_df["price"].apply(lambda x: '{:.5f}'.format(x))
    
    dataset_df.to_csv(
        path_temp_csv,
        index=False
    )

def _load():
    engine_mysql = sqlalchemy.create_engine('mysql+pymysql://root:airflow@host.docker.internal:3308/crypto')

    dataset_df = pd.read_csv(path_temp_csv)

    dataset_df.to_sql("coins", engine_mysql, if_exists="replace",index=False)

extract_API_task = PythonOperator(
    task_id="Extract_API_Data", 
    python_callable=_extract,
    dag=dag
)

transform_task = PythonOperator(
    task_id="Transform_Dataset",
    python_callable=_transform, 
    dag=dag
)

load_task = PythonOperator(
    task_id="Load_Dataset",
    python_callable=_load,
    dag=dag
)

clean_task = BashOperator(
    task_id="Clean",
    bash_command="scripts/clean.sh",
    dag=dag
)


extract_API_task >> transform_task >> load_task >> clean_task

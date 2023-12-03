from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from reddit_etl import RunRedditETL


cfg = {
    'sub': 'python',
    'credentials_path': 'credentials/keys.json',
    'limit': 10,
    'output_folder': 'output',
}

def perform_reddit_etl():
    reddit_etl = RunRedditETL(sub=cfg['sub'], credentials_path=cfg['credentials_path'], limit=cfg['limit'], output_folder=cfg['output_folder'])
    df = reddit_etl.start()
    return df

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'reddit_dag',
    default_args=default_args,
    description='Reddit DAG with ETL process!',
    schedule_interval=timedelta(days=1),
)


run_etl = PythonOperator(
    task_id='complete_reddit_etl',
    python_callable=perform_reddit_etl,
    provide_context=True,
    dag=dag,
)

run_etl
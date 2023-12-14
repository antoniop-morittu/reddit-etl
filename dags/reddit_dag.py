"""
This DAG is used to run the ETL process for the Reddit API. The main objective is to retrieve the top 10 posts from any subreddit and save it in a CSV file or store in a database.
"""
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from custom.etl import extract, transform
from custom.tools import GeneratorID
import os

DATA_DIRECTORY = os.path.join(os.getcwd(), "data")
print(DATA_DIRECTORY)
PATH_CREDENTIALS = os.path.join(os.getcwd(), "config/credentials/keys.json")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 11, 8),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 5,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    "reddit_dag",
    default_args=default_args,
    start_date=datetime(year=2023, month=12, day=11),
    description="Reddit DAG with ETL process!",
    schedule_interval=timedelta(days=1),
) as dag:

    def perform_etl_task(**kwargs):
        import os

        post_type = kwargs.get("post_type")
        # Create a directory to save the data
        os.makedirs(f"{DATA_DIRECTORY}/{post_type}", exist_ok=True)
        kwargs[
            "save_path"
        ] = f"{DATA_DIRECTORY}/{post_type}/{GeneratorID.id_number_generator()}.csv"

        extract_df = extract(**kwargs)

        return transform(extract_df, **kwargs).to_json()

    parameters = {
        "sub": "solana",
        "limit": 10,
        "credentials_path": PATH_CREDENTIALS,
        "post_type": "get_new_posts",
    }

    extract_and_transform_data = PythonOperator(
        task_id="extract_and_transform_data",
        python_callable=perform_etl_task,
        op_kwargs=parameters,
        provide_context=True,
    )

extract_and_transform_data

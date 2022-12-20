import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.exceptions import AirflowSkipException
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################

csv_file = "/usr/local/spark/resources/data/bank-additional-full.csv"
cleansed_file = "/usr/local/spark/resources/data/spark_output/bank-additional-full.csv"
dataset_csv_file = "bank-additional-full.csv"
dbt_loc = "/usr/local/dbt/bank_campaign_dwh"

GOOGLE_APPLICATION_CREDENTIALS = "/home/.google/credentials/google_credentials.json"
AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT = "google-cloud-platform://?extra__google_cloud_platform__key_path=/home/.google/credentials/google_credentials.json"
project_id = "finalproject-kulidata"
bucket_name = "finalproject-kulidata"
dataset_id = "rawdata"

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
        dag_id="coba", 
        description="This DAG is end-to-end batch processing data pipeline from ingestion to dbt",
        default_args=default_args, 
        schedule_interval=timedelta(1)
    )

start = DummyOperator(task_id="start", dag=dag)

run_dbt_task = BashOperator(
    task_id="run_dbt",
    bash_command= f"cd {dbt_loc}"
        + " && dbt run --profiles-dir /usr/local/dbt",
    dag=dag,
)

end = DummyOperator(task_id="end", dag=dag)

start >> run_dbt_task >> end
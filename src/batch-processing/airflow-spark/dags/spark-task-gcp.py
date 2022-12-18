import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

from google.cloud import storage
from airflow.contrib.operators.bigquery_operator import BigQueryCreateExternalTableOperator

###############################################
# Parameters
###############################################
spark_master = "spark://spark:7077"
postgres_driver_jar = "/usr/local/spark/resources/jars/postgresql-9.4.1207.jar"

csv_file = "/usr/local/spark/resources/data/bank-additional-full.csv"
cleansed_file = "/usr/local/spark/resources/data/spark_output/bank-additional-full.csv"
dataset_csv_file = "bank-additional-full.csv"

postgres_db = "jdbc:postgresql://postgres/test"
postgres_user = "test"
postgres_pwd = "postgres"

# PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
# BUCKET = os.environ.get("GCP_GCS_BUCKET")
# BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'rawdata')

GOOGLE_APPLICATION_CREDENTIALS = "/home/.google/credentials/google_credentials.json"
AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT = "google-cloud-platform://?extra__google_cloud_platform__key_path=/home/.google/credentials/google_credentials.json"
project_id = "finalproject-kulidata"
bucket_name = "finalproject-kulidata"

###############################################
# DAG Definition
###############################################
now = datetime.now()

def upload_to_gcs(bucket, object_name, local_file):
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client(project_id)
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

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
        dag_id="spark-task-gcp", 
        description="This DAG is a sample of integration between Spark and DB. It reads CSV files, load them into a Postgres DB and then read them from the same Postgres DB.",
        default_args=default_args, 
        schedule_interval=timedelta(1)
    )

start = DummyOperator(task_id="start", dag=dag)

ingest_bank_marketing_data = BashOperator(
    task_id="ingest_bank_marketing_data",
    bash_command="bash /usr/local/spark/resources/bin/download_data.sh ",
    dag=dag,
)

unzip_file = BashOperator(
    task_id="unzip_file",
    bash_command="bash /usr/local/spark/resources/bin/unzip_file.sh ",
    dag=dag,
)

spark_cleanse_job = SparkSubmitOperator(
    task_id="spark_cleanse",
    application="/usr/local/spark/app/spark-cleansing.py",
    name="spark-cleansing",
    conn_id="spark_default",
    verbose=1,
    conf={"spark.master":spark_master},
    application_args=[csv_file],
    dag=dag
)

local_to_gcs_task = PythonOperator(
    task_id="upload_to_gcs_task",
    python_callable=upload_to_gcs,
    op_kwargs={
        "bucket": bucket_name,
        "local_file": f"{cleansed_file}",
        "object_name": f"raw/{dataset_csv_file}",
    },
    dag=dag
)

bigquery_external_table_task = BigQueryCreateExternalTableOperator(
    task_id="bigquery_external_table_task",
    source_objects=[f"gs://{bucket_name}/raw/{dataset_csv_file}"],
    destination_project_dataset_table="rawdata.bank_marketing",
    bucket=bucket_name,
    table_resource={
            "externalDataConfiguration": {
                "sourceFormat": "CSV",
                "sourceUris": [f"gs://{bucket_name}/raw/{dataset_csv_file}"],
            },        
    },
    dag=dag
)

end = DummyOperator(task_id="end", dag=dag)

start >> ingest_bank_marketing_data >> unzip_file >> spark_cleanse_job >> local_to_gcs_task >> bigquery_external_table_task >> end
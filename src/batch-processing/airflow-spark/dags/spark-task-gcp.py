import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.exceptions import AirflowSkipException
from datetime import datetime, timedelta

from google.cloud import storage
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

###############################################
# Parameters
###############################################
spark_master = "spark://spark:7077"

csv_file = "/usr/local/spark/resources/data/bank-additional-full.csv"
cleansed_file = "/usr/local/spark/resources/data/spark_output/bank-additional-full.csv"
dataset_csv_file = "bank-additional-full.csv"
dbt_loc = "/usr/local/dbt/bank_campaign_dwh"

GOOGLE_APPLICATION_CREDENTIALS = "/home/.google/credentials/google_credentials.json"
AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT = "google-cloud-platform://?extra__google_cloud_platform__key_path=/home/.google/credentials/google_credentials.json"
project_id = "finalproject-kulidata"
bucket_name = "finalproject-kulidata"
dataset_id = "rawdata"

query = """CREATE OR REPLACE EXTERNAL TABLE rawdata.bank_marketing
OPTIONS(
  format = 'CSV',
  uris = ['gs://finalproject-kulidata/raw/bank-additional-full.csv']) """

query2 = """CREATE OR REPLACE TABLE
  finalproject-kulidata.bank_campaign_dwh.fact_bank_partitioned
PARTITION BY 
  RANGE_BUCKET(job_id,GENERATE_ARRAY(1,12,1))
CLUSTER BY
  education_id
AS
  SELECT * FROM finalproject-kulidata.bank_campaign_dwh.fact_bank"""

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
        description="This DAG is end-to-end batch processing data pipeline from ingestion to dbt",
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

bigquery_external_table_task = BigQueryOperator(
    task_id="bigquery_external_table_task",
    sql=query,
    use_legacy_sql=False,
    dag=dag,
)

run_dbt_task = BashOperator(
    task_id="run_dbt",
    bash_command= f"cd {dbt_loc}"
        + " && dbt run --profiles-dir /usr/local/dbt",
    dag=dag,
)

bigquery_partition_cluster_table_task = BigQueryOperator(
    task_id="bigquery_partition_cluster_table_task",
    sql=query2,
    use_legacy_sql=False,
    dag=dag,
)

end = DummyOperator(task_id="end", dag=dag)

start >> ingest_bank_marketing_data >> unzip_file >> spark_cleanse_job >> local_to_gcs_task >> bigquery_external_table_task >> run_dbt_task >> bigquery_partition_cluster_table_task >> end
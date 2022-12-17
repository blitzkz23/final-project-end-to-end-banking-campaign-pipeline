from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################
spark_master = "spark://spark:7077"
postgres_driver_jar = "/usr/local/spark/resources/jars/postgresql-9.4.1207.jar"

fhv_trip_file = "/usr/local/spark/resources/data/fhv_tripdata_2021-02.parquet"

postgres_db = "jdbc:postgresql://postgres/test"
postgres_user = "test"
postgres_pwd = "postgres"

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

# spark_job_load_postgres = SparkSubmitOperator(
#     task_id="spark_job_load_postgres",
#     application="/usr/local/spark/app/load-postgres.py", # Spark application path created in airflow and spark cluster
#     name="load-postgres",
#     conn_id="spark_default",
#     verbose=1,
#     conf={"spark.master":spark_master},
#     application_args=[movies_file,ratings_file,postgres_db,postgres_user,postgres_pwd],
#     jars=postgres_driver_jar,
#     driver_class_path=postgres_driver_jar,
#     dag=dag)

end = DummyOperator(task_id="end", dag=dag)

start >> ingest_bank_marketing_data >> end
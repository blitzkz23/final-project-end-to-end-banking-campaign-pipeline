## General Installation Guide/Usage

### Batch Processing
====================
- Prerequisite:

    A. Python 3: [Install Here](https://www.python.org/downloads/)
    
    B. Docker and Docker Compose: [Install Here](https://docs.docker.com/engine/install/ubuntu/)
    
    C. Google's Credential Service Account used for GCS and Bigquery access: [Get Here](https://developers.google.com/workspace/guides/create-credentials)
    
    D. DBT Core and Bigquery Dependency: [Install Here](https://docs.getdbt.com/docs/get-started/pip-install)
    
    Rename the google credentials into `google_credentials.json` and store it in your `$HOME` directory

- Project Guide:

    A. Clone this project
            
        git clone https://github.com/blitzkz23/final-project-end-to-end-banking-campaign-pipeline.git
        
    B. Open this project in terminal and change directory until docker-airflow folder, also build the docker file
        
        # change directory
        cd src/batch-processing/docker/docker-airflow

        # run build docker
        docker build --rm --build-arg AIRFLOW_DEPS="gcp" -t docker-airflow-spark:1.10.7_3.1.2 .
        

    C. After docker build complete, return to previous directory and run docker compose, then wait for a few minutes for all the container to be up

        docker compose up
        

    D. Open the airflow webserver UI on external-IP:8282 / localhost:8282 (if you have ports forwarding)
    
    E. Configure spark connection acessing airflow web UI http://localhost:8282 and going to Connections
            ![](./docs/airflow_connections_menu.png "Airflow Connections")

    F. Edit the spark_default connection inserting `spark://spark` in Host field and Port `7077`
            ![](./docs/airflow_spark_connection.png "Airflow Spark connection")

    G. Also edit the bigquery_default connection, and insert your project name:
            ![](./docs/airflow_bigquery_connection.png "Airflow BigQuery connection")

    H. Airflow DAGs for batch processing is ready to go! included task on the DAG are up to uploading data from gcs to BigQuery table, unfortunately the dbt transformation are not included yet on the DAGs because of the dependencies conflict.  But afraid not its simple enough, follow the next step.

    I. You need to set up few dbt-related config, such as:
    - Create profiles.yml on ~/.dbt or /home/usr/.dbt directory.  Refer to this [example](https://docs.getdbt.com/reference/profiles.yml)
    - Generate google-credentials.json from service account that have accesss to bigquery

    J. Assuming you are still on docker directory, do:
       
       
        # return to prev dir
        cd ..

        cd dbt

        cd bank_campaign_dwh

        # run dbt
        dbt run

### Stream Processing
=====================

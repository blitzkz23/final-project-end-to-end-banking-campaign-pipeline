# Dokcer Setting

```bash
sudo docker build -t kafka-connect-spooldir .
```

```bash
docker compose up
```

# Check CSV connector

```bash
curl -s localhost:8083/connector-plugins|jq '.[].class'|egrep 'SpoolDir'
```

# Loading data from CSV to Kafka

```bash
curl -i -X PUT -H "Accept:application/json" \
    -H  "Content-Type:application/json" http://localhost:8083/connectors/csv-source/config \
    -d '{
        "connector.class" : "com.github.jcustenborder.kafka.connect.spooldir.SpoolDirCsvSourceConnector",
        "input.path": "/usr/local/kafka/data/unprocessed",
        "finished.path": "/usr/local/kafka/data/processed",
        "error.path": "/usr/local/kafka/data/error",
        "input.file.pattern": ".*\\.csv",
        "topic" : "csv_spooldir_00",
        "schema.generation.key.fields":"age",
        "csv.first.row.as.header":"true",
        "transforms":"castTypes",
        "transforms.castTypes.type":"org.apache.kafka.connect.transforms.Cast$Value",
        "transforms.castTypes.spec":"age:int32,job:string,marital:string,education:string,default:string,housing:string,loan:string,contact:string,month:string,day_of_week:string,duration:int32,campaign:int32,pdays:int32,previous:int32,poutcome:string,emp_var_rate:float32,cons_price_idx:float32,cons_conf_idx:float32,euribor3m:float32,nr_employed:int64,y:string"
		}'
```
# Check Bigquery connector

```bash
curl -sS localhost:8083/connector-plugins | jq .[].class | grep BigQuerySinkConnector
```
# Sink CSV data to BigQuery

```bash
curl -X PUT http://localhost:8083/connectors/bigquery-sink-connector/config \
    -H "Content-Type: application/json" \
    -d '{
        "connector.class": "com.wepay.kafka.connect.bigquery.BigQuerySinkConnector",
        "topics": "csv_spooldir_00",
        "project": "FinalProject-kulidata",
        "defaultDataset": "stream",
        "sanitizeTopics" : "true",
        "autoCreateTables" : "true",
        "allowNewBigQueryFields" : "true",
        "allowBigQueryRequiredFieldRelaxation" : "true",
        "schemaRetriever" : "com.wepay.kafka.connect.bigquery.retrieve.IdentitySchemaRetriever",
        "keyfile": "usr/local/kafka/data/google_credentials.json"
    }'
```

# ksqlDB

CREATE STREAM BANK_MARKETING_CSV WITH (KAFKA_TOPIC='orders_spooldir_00',VALUE_FORMAT='AVRO'); #Create stream

DESCRIBE BANK_MARKETING_CSV; #Check the schema



# Relevant Commands

+ curl -X DELETE http://localhost:8083/connectors/bigquery-sink-connector

+ curl -X DELETE http://localhost:8083/connectors/source-csv-spooldir-00

+ sudo docker exec broker kafka-topics --delete --zookeeper zookeeper:2181 --topic csv_spooldir_00

+ sudo docker exec broker kafka-topics --list --zookeeper zookeeper:2181

+ sudo docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

+ sudo docker exec -it postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB'

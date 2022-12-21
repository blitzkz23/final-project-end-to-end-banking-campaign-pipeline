import sys
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import when
from pyspark.sql.functions import regexp_replace

import pandas as pd
import numpy as np

# Create spark session
spark = (SparkSession
    .builder 
    .appName("spark-cleansing") 
    .getOrCreate()
    )
sc = spark.sparkContext
sc.setLogLevel("WARN")

####################################
# Parameters
####################################
csv_file = sys.argv[1]

####################################
# Read CSV Data
####################################
print("######################################")
print("READING CSV FILE")
print("######################################")

df_bank_marketing = (
    spark.read
    .format("csv")
    .option("sep", ";")
    .option("header", True)
    .load(csv_file)
)

####################################
# Format Standarization
####################################
print("######################################")
print("FORMAT STANDARIZATION")
print("######################################")
# Rename column with dots (.), because spark cant read them
df_transform1 = df_bank_marketing.withColumnRenamed('emp.var.rate', 'emp_var_rate') \
    .withColumnRenamed('cons.price.idx', 'cons_price_idx') \
    .withColumnRenamed('cons.conf.idx', 'cons_conf_idx') \
    .withColumnRenamed('nr.employed', 'nr_employed')

# Rename education column value from basic.4y, basic.6y, basic.6y into basic
df_transform2 = df_transform1.withColumn("education",
                                        when(df_transform1.education.endswith('4y'), regexp_replace(df_transform1.education, 'basic.4y', 'basic')) \
                                        .when(df_transform1.education.endswith('6y'), regexp_replace(df_transform1.education, 'basic.6y', 'basic')) \
                                         .when(df_transform1.education.endswith('9y'), regexp_replace(df_transform1.education, 'basic.9y', 'basic')) \
                                         .otherwise(df_transform1.education)
                                        )

# Rename default column name into credit
df_transform3 = df_transform2.withColumnRenamed("default", "credit")

# Add year to month 
df_transform4 = df_transform3.withColumn("month",
                                         when(df_transform3.month.endswith('jan'), regexp_replace(df_transform3.month, 'jan', '200801')) \
                                            .when(df_transform3.month.endswith('feb'), regexp_replace(df_transform3.month, 'feb', '200802')) \
                                                .when(df_transform3.month.endswith('mar'), regexp_replace(df_transform3.month, 'mar', '200803')) \
                                                    .when(df_transform3.month.endswith('apr'), regexp_replace(df_transform3.month, 'apr', '200804')) \
                                                        .when(df_transform3.month.endswith('may'), regexp_replace(df_transform3.month, 'may', '200805')) \
                                                            .when(df_transform3.month.endswith('jun'), regexp_replace(df_transform3.month, 'jun', '200806')) \
                                                                .when(df_transform3.month.endswith('jul'), regexp_replace(df_transform3.month, 'jul', '200807')) \
                                                                    .when(df_transform3.month.endswith('aug'), regexp_replace(df_transform3.month, 'aug', '200808')) \
                                                                        .when(df_transform3.month.endswith('sep'), regexp_replace(df_transform3.month, 'sep', '200809')) \
                                                                            .when(df_transform3.month.endswith('oct'), regexp_replace(df_transform3.month, 'oct', '200810')) \
                                                                                .when(df_transform3.month.endswith('nov'), regexp_replace(df_transform3.month, 'nov', '200811')) \
                                                                                    .when(df_transform3.month.endswith('dec'), regexp_replace(df_transform3.month, 'dec', '200812')) \
                                                                                        .otherwise(df_transform3.month)
                                         
                                         )

####################################
# Cleanse Null Data
####################################
print("######################################")
print("CLEANSE NULL DATA")
print("######################################")
df_transform5 = df_transform4.na.drop("all")

####################################
# Save Data
####################################
print("######################################")
print("SAVE DATA")
print("######################################")
df_transform5.coalesce(1).write \
      .option("header","true") \
      .option("sep",",") \
      .mode("overwrite") \
      .csv("/usr/local/spark/resources/data/spark_output/")

df_transform5.toPandas().to_csv("/usr/local/spark/resources/data/spark_output/bank-additional-full.csv", index=False)  
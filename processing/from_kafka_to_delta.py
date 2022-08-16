from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

# set conf
conf = (
SparkConf()
    .set("spark.hadoop.fs.s3a.fast.upload", True)
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .set("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.EnvironmentVariableCredentialsProvider")
    .set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()

spark = (
    SparkSession.builder
    .appName("ConsumeFromKafka")
    .getOrCreate()
)

spark.sparkContext.setLogLevel('ERROR')

sales = (
    spark.readStream
    .format('kafka')
    .option("kafka.bootstrap.servers", "10.100.247.158:9092") # CHANGE HOST FOR YOUR KAFKA CLUSTER!!
    .option("subscribe", "mssql-sales")
    .option("startingOffsets", "earliest")
    .load()
)

sales.printSchema()

# schema = StructType([
#     StructField("NOME", StringType(), False),
#     StructField("SEXO", StringType(), False),
#     StructField("TELEFONE", StringType(), False),
#     StructField("NASCIMENTO", StringType(), False),
#     StructField("DT_UPDATE", StringType(), False)
# ])

schema1 = StructType([
    StructField("schema", StringType(), False),
    StructField("payload", StringType(), False)
])

schema2 = StructType([
    StructField("userid", IntegerType(), False),
    StructField("productid", IntegerType(), False),
    StructField("quantity", IntegerType(), False),
    StructField("price", StringType(), False),
    StructField("paymentmtd", IntegerType(), False),
    StructField("paymentsts", IntegerType(), False),
    StructField("dt_insert", StringType(), False),
    StructField("dt_update", TimestampType(), False)
])


o = sales.selectExpr("CAST(value AS STRING)")

#o.writeStream.format("console").outputMode("append").option("truncate", False).start().awaitTermination()

o2 = o.select(f.from_json(f.col("value"), schema1).alias("data")).selectExpr("data.payload")
o2 = o2.selectExpr("CAST(payload AS STRING)")
novo = o2.select(f.from_json(f.col("payload"), schema2).alias("data")).selectExpr("data.*")
# #novo = df.select(from_avro(f.col("value"), jsonFormatSchema=schema).alias("data")).selectExpr("data.*")

novo.printSchema()

consulta = (
    novo
    .groupBy("userid")
    .agg(
        f.count("productid").alias("numberofpurchases")
    )
)

(
    consulta
    .writeStream
    .format("delta")
    .outputMode("complete")
    .option("checkpointLocation", "s3a://dl-processing-zone-539445819060/sales_domain/kafka_events/checkpoint_sales_per_user")
    .start("s3a://dl-processing-zone-539445819060/sales_domain/kafka_events/mssql-sales-per-user/")
    .awaitTermination()
)

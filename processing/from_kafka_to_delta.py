from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .appName("ConsumeFromKafka")
    .getOrCreate()
)

spark.sparkContext.setLogLevel('ERROR')

df = (
    spark.readStream
    .format('kafka')
    .option("kafka.bootstrap.servers", "acba6cbedb2ff4611b9fcad4dceb7924-455506638.us-east-1.elb.amazonaws.com:9094")
    .option("subscribe", "src-mssql-vehicle2")
    .option("startingOffsets", "earliest")
    .load()
)

df.printSchema()

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
    StructField("id", IntegerType(), False),
    StructField("customerid", IntegerType(), False),
    StructField("ano_modelo", StringType(), False),
    StructField("modelo", StringType(), False),
    StructField("fabricante", StringType(), False),
    StructField("ano_veiculo", StringType(), False),
    StructField("categoria", StringType(), False),
])


o = df.selectExpr("CAST(value AS STRING)")

#o.writeStream.format("console").outputMode("append").option("truncate", False).start().awaitTermination()

o2 = o.select(f.from_json(f.col("value"), schema1).alias("data")).selectExpr("data.payload")
o2 = o2.selectExpr("CAST(payload AS STRING)")
novo = o2.select(f.from_json(f.col("payload"), schema2).alias("data")).selectExpr("data.*")
# #novo = df.select(from_avro(f.col("value"), jsonFormatSchema=schema).alias("data")).selectExpr("data.*")

novo.printSchema()

(
    novo
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "s3://dl-landing-zone-539445819060/kafka-events/mssql/checkpoint_vehicle")
    .start("s3://dl-landing-zone-539445819060/kafka-events/mssql/vehicle")
    .awaitTermination()
)

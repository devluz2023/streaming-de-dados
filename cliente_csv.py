from pyspark.sql import SparkSession
from pyspark.sql import functions as f
import shutil

for item in ['./check', './csv']:
    try:
        shutil.rmtree(item)
    except OSError as err:
        print(f'Aviso:{err.strerror}')

spark = SparkSession.builder.appName('SparkStreaming').getOrCreate()
tweets = spark.readStream\
    .format('socket')\
    .option('host', 'localhost')\
    .option('port', 9010)\
    .load()

words = tweets.select(f.explode(f.split(tweets.value, ' ')).alias('word'))
wordCounts = words.groupBy('word').count()


query = tweets.writeStream\
    .outputMode('append')\
    .option('encoding', 'utf-8')\
    .format('csv')\
    .option('path', './csv')\
    .option('checkpointLocation', './check')\
    .format('console')\
    .start()

query.awaitTermination()
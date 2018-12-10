#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: KafkaProducer.py 
@time: 18-6-23 下午7:44 
"""
from threading import Thread
from time import sleep

from pyspark import SparkConf, SparkContext, SQLContext, HiveContext
from pykafka import KafkaClient

if __name__ == "__main__":
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    conf = SparkConf().setAppName('Kafka').setMaster(clusterMasterURL) \
        .set('spark.executor.memory', '7G')
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    testDF = hc.sql('select * from testData limit 10000')
    prop = {
        'bootstrap.servers': 'Master:9092',
        'key.serializer': 'org.apache.kafka.common.serialization.StringSerializer',
        'value.serializer': 'org.apache.kafka.common.serialization.StringSerializer'
    }
    testDF.show()

    topic = 'movie'
    testData = testDF.rdd.map(
        lambda x: (topic, str(int(x[0])) + ',' + str(int(x[1])) + ',' + str(float(x[2])))
    ).toDF()

    testData.show()

    client = KafkaClient(hosts='Master:9092')
    # 如果服务器内存不够, 会出现OOM错误
    messages = testData.toLocalIterator()

    topicdocu = client.topics[b'movie']
    producer = topicdocu.get_producer()
    for message in messages:
        print(topic, message[0], message[1])
        producer.produce(message[0].encode(encoding="utf-8") + message[1].encode(encoding="utf-8"))
        sleep(10)
    producer.stop()
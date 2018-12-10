#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ConsumerTest.py 
@time: 18-6-23 下午8:23 
"""
from pykafka import KafkaClient

client = KafkaClient(hosts='Master:9092')
topicdocu = client.topics['movie'.encode(encoding="utf-8")]
consumer = topicdocu.get_simple_consumer(consumer_group='movie'.encode(encoding="utf-8"))
for message in consumer:
    if message is not None:
        print(message.offset, message.value)
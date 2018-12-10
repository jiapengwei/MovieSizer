#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: RatingData.py 
@time: 18-6-20 上午1:52 
"""

import os

from pyspark import SparkContext, SparkConf, SQLContext, HiveContext

if __name__ == "__main__":
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    print(os.environ['SPARK_HOME'])
    print(os.environ['HADOOP_HOME'])
    conf = SparkConf().setAppName("RatingData").setMaster(clusterMasterURL)
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    ratings = hc.cacheTable('ratings')
    count = hc.sql("select count(*) from ratings").first()[0]

    # 将数据分割成训练集和测试集
    percent = 0.6
    trainingDataCount = int((count * percent))
    testDataCount = int(count * (1 - percent))

    # 评分数据按时间升序排列
    trainingDataASC = hc.sql('select userId,movieId,rating from ratings order by ts asc')
    trainingDataASC.write.mode('overwrite').saveAsTable('trainingDataASC')

    # 评分数据按时间降序排列
    trainingDataDESC = hc.sql('select userId,movieId,rating from ratings order by ts desc')
    trainingDataDESC.write.mode('overwrite').saveAsTable('trainingDataDESC')

    # 60% 的数据作为训练模型
    trainingData = hc.sql('select * from trainingDataAsc limit %d ' % trainingDataCount)
    trainingData.write.mode('overwrite').saveAsTable('trainingData')

    # 40% 作为测试模型
    testData = hc.sql('select * from trainingDataDesc limit %d' % testDataCount)
    testData.write.mode('overwrite').saveAsTable('testData')
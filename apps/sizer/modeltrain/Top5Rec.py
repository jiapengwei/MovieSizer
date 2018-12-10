#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Top5Rec.py 
@time: 18-6-21 下午11:04 
"""
import datetime

from pyspark import HiveContext, SQLContext, SparkContext, SparkConf
from pyspark.sql.functions import udf

jdbcURL = "jdbc:mysql://Master:3306/recommend?useUnicode=true&characterEncoding=utf-8&useSSL=false"

top5Table = "MovieSizer.operation_defaultpop5result"
prop = {
    'dirver': 'com.mysql.jdbc.Driver',
    'user': 'root',
    'password': 'woshiwo111'
}

if __name__ == "__main__":
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    conf = SparkConf().setAppName('Top5Recommending').setMaster(clusterMasterURL) \
        .set('spark.executor.memory', '7G')
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    pop = hc.sql("select count(*) as c ,movieId from trainingData group by movieId order by c desc")
    pop5 = pop.select('movieId').limit(5).selectExpr('movieId as movie_id')
    pop5.registerTempTable('pop5')

    datetimeCol = udf(lambda x: str(datetime.date.today()))
    pop5res = pop5.withColumn('redate', datetimeCol('movie_id'))
    pop5res.show()
    # pop5Result = hc.sql('select a.movieId,a.title from movies a join pop5 b where a.movieId=b.movieId')
    #
    # pop5Result.write.jdbc(url=jdbcURL, table=top5Table, properties=prop, mode='append')
    pop5res.write.jdbc(url=jdbcURL, table=top5Table, properties=prop, mode='append')
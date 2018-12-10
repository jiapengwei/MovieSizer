#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ItemCF.py 
@time: 18-6-22 下午4:24 
"""
from pyspark import HiveContext, SQLContext, SparkContext, SparkConf

from sizer.modeltrain import ItemSimilarity

jdbcURL = "jdbc:mysql://Master:3306/recommend?useUnicode=true&characterEncoding=utf-8&useSSL=false"
recResultTable = "MovieSizer.movies_moviesimilar"
prop = {
    'dirver': 'com.mysql.jdbc.Driver',
    'user': 'root',
    'password': 'woshiwo111'
}
if __name__ == '__main__':
    """
        根据ratings表，生成电影相似度表
    """
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    conf = SparkConf().setAppName('ItemCF').setMaster(clusterMasterURL) \
        .set('spark.executor.memory', '7G')
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    # 读取数据并cache到内存中
    ratings = hc.sql('select * from ratings').cache()
    # ratings.show()

    # 建立模型
    simil_rdd1 = ItemSimilarity.similarity(ratings.rdd, 'coocurrence')
    # simil_rdd1.show()
    simil_res = simil_rdd1.toDF(['item1', 'item2', 'similar'])
    simil_res.write.jdbc(url=jdbcURL, table=recResultTable, properties=prop, mode='append')
    # simil_rdd1.foreach(print)
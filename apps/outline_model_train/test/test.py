#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: test.py 
@time: 18-6-25 下午8:05 
"""
from pyspark import SparkConf, SparkContext, SQLContext, HiveContext


if __name__ == '__main__':
        localClusterURL = "local[2]"
        clusterMasterURL = "spark://Master:7077"
        conf = SparkConf().setAppName('ELT').setMaster(localClusterURL)
        sc = SparkContext.getOrCreate(conf)
        sqlContext = SQLContext(sc)
        hc = HiveContext(sc)

        rating_tab = 'MovieSizer.operation_rating'

        jdbcURL = "jdbc:mysql://Master:3306/recommend?useUnicode=true&characterEncoding=utf-8&useSSL=false"

        prop = {
            'dirver': 'com.mysql.jdbc.Driver',
            'user': 'root',
            'password': 'woshiwo111'
        }
        #  user\rating\links\tags在hdfs中的位置 ===> 即推荐原料在hdfs中的存档路径
        hdfs_data_path = 'hdfs://Master:9000/movie/data/'
        hdfs_rating_tab = hdfs_data_path + 'ratings.txt'

        # 从hive中读取rating数据到mysql中
        ratingDF = hc.sql('select * from moviesizer.ratings')\
            .selectExpr(
                'movieId as movie_id',
                'userId as user_id',
                'ts as ds',
                'rating as rating'
            )

        print(type(ratingDF))

        ratingDF.write.jdbc(url=jdbcURL, table=rating_tab, properties=prop, mode='append')
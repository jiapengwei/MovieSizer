#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: AppConf.py 
@time: 18-6-25 下午2:59 
"""

import os

from pyspark import SparkConf, SparkContext, SQLContext, HiveContext


class AppConf:
    def __init__(self):
        self.localClusterURL = "local[2]"
        self.clusterMasterURL = "spark://Master:7077"
        self.conf = SparkConf().setMaster(self.clusterMasterURL)
        self.sc = SparkContext.getOrCreate(self.conf)
        self.sqlContext = SQLContext(self.sc)
        self.hc = HiveContext(self.sc)

        self.jdbcURL = "jdbc:mysql://Master:3306/recommend?useUnicode=true&characterEncoding=utf-8&useSSL=false"

        self.prop = {
            'dirver': 'com.mysql.jdbc.Driver',
            'user': 'root',
            'password': 'woshiwo111'
        }
        #  user\rating\links\tags在hdfs中的位置 ===> 即推荐原料在hdfs中的存档路径
        self.hdfs_data_path = 'hdfs://Master:9000/movie/data/'
        self.movies_path = self.hdfs_data_path + 'movies.txt'
        self.ratings_path = self.hdfs_data_path + 'ratings.txt'
        self.links_path = self.hdfs_data_path + 'links.txt'
        self.tags_path = self.hdfs_data_path + 'tags.txt'

        # 各种result数据在mysql中的表
        self.default5Table = 'MovieSizer.operation_default5recommend'
        self.top5Table = 'MovieSizer.oertion_top5recomm'

        self.alsTable = 'MovieSizer.movies_alsTab'
        self.similarTable = 'MovieSizer.movies_movidesimilar'
        self.usesrTable = 'MovieSizer.usesr_userprofile'
        self.ratingTable = 'MovieSizer.operation_rating'

        self.movieTab = 'MovieSizer.movies_movieinfo'

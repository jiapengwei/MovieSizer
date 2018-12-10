#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
    用于创建Spark程序入口, 供其他程序继承
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: AppConf.py 
@time: 18-6-20 下午12:47 
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


        # self.alsTable = "recommend.alsTab"
        # self.recResultTable = "recommend.similarTab"
        # self.top5Table = "MovieSizer.operation_defaultpop5result"
        # self.userTable = "recommend.user"
        # self.ratingTable = "recommend.rating"

        self.alsTable = 'MovieSizer.movies_alsTab'
        self.similarTable = 'MovieSizer.movies_movidesimilar'
        self.top5Table = 'MovieSizer.oertion_top5recomm'
        self.usesrTable = 'MovieSizer.usesr_userprofile'
        self.ratingTable = 'MovieSizer.operation_rating'


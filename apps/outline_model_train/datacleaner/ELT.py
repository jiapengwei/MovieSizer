#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ELT.py 
@time: 18-6-25 下午3:12 
"""
import string

from pyspark import SparkConf, SparkContext, SQLContext, HiveContext

from outline_model_train.conf.AppConf import AppConf
from outline_model_train.caseclass.models import Link, Movie, Tag, Rating


# hive 服务启动命令
# nohup hive --service metastore > metastore.log 2>&1 &
def movie_str_rebuild(inStr: string):
    a = inStr.split(',')
    head = a[0]
    tail = a[-1]
    a.pop()
    a.pop(0)
    bo = ' '.join(a).replace('"', '').replace("'", '').replace(',', ' ')
    return head + ',' + bo + ',' + tail


def tag_str_rebuild(inStr: string):
    a = inStr.split(',')
    head = ','.join(a[:2])
    tail = str(a[-1])
    a.pop()
    a.pop(0)
    a.pop(0)
    bo = ' '.join(a).replace('"', '').replace("'", '')
    return head + ',' + bo + ',' + tail


class ELT():
    def __init__(self):
        self.localClusterURL = "local[2]"
        self.clusterMasterURL = "spark://Master:7077"
        self.conf = SparkConf().setAppName('ELT').setMaster(self.localClusterURL)
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
        self.tagTab = 'MovieSizer.movies_movieinfo_typelist'

        # 设置RDD的partition的数量一般以集群分配给应用的CPU核数的整数倍为宜。
        self.minPartitions = 8

    def loadLinks2HV(self):
        """
            将links数据从hdfs中加载保存到hive中
        :return:
        """
        links = self.sc.textFile(self.links_path, self.minPartitions).filter(
            lambda x: not x.endswith(',')) \
            .map(lambda x: x.split(',')).map(
            lambda x: Link(int(x[0].strip()), int(x[1].strip()), int(x[2].strip()))).toDF()

        # 通过数据写入到HDFS，将表存到hive中
        # links
        links.write.mode('overwrite').saveAsTable('MovieSizer.links')

    def loadMovies2Hive(self):
        """
            将movies数据从hdfs中加载保存到hive中
        :return:
        """
        # movies = self.sc.textFile(self.movies_path, self.minPartitions).filter(
        #     lambda x: not x.endswith(',')) \
        #     .map(lambda x: movie_str_rebuild(x)).map(lambda x: x.split(',')).map(
        #     lambda x: Movie(int(x[0]), str(x[1]), str(x[2]))).toDF()

        # 离线计算时从mysql加载movies数据到hive中
        movies_sql = self.sqlContext.read.format('jdbc') \
            .options(url=self.jdbcURL,
                     driver=self.prop['dirver'],
                     dbtable=self.movieTab,
                     user=self.prop['user'],
                     password=self.prop['password']).load()

        movies = movies_sql.select(['id', 'moviename'])

        # 通过数据写入到HDFS，将表存到hive中
        # links
        movies.write.mode('overwrite').saveAsTable('MovieSizer.movies')

    def loadTags2Hive(self):
        """
            将tags数据从hdfs加载保存到hive中
        :return:
        """
        # tags = self.sc.textFile(self.tags_path, self.minPartitions).filter(
        #     lambda x: not x.endswith(',')) \
        #     .map(lambda x: tag_str_rebuild(x)).map(lambda x: x.split(',')).map(
        #     lambda x: Tag(int(x[0].strip()), int(x[1].strip()), str(x[2].strip()), int(x[3].strip()))).toDF()

        # 离线计算时从mysql中加载tags到hive中
        tags_sql = self.sqlContext.read.format('jdbc') \
            .options(url=self.jdbcURL,
                     driver=self.prop['dirver'],
                     dbtable=self.tagTab,
                     user=self.prop['user'],
                     password=self.prop['password']).load()

        tags = tags_sql.select(['id', 'movieinfo_id', 'moviecategory_id'])
        tags.write.mode('overwrite').saveAsTable('MovieSizer.tags')

    def loadRatings2Hive(self):
        """
            将ratings数据从hdfs加载保存到hive中
        :return:
        """
        # ratings = self.sc.textFile(self.ratings_path, self.minPartitions).filter(
        #     lambda x: not x.endswith(',')) \
        #     .map(lambda x: x.split(',')).map(
        #     lambda x: Rating(int(x[0].strip()), int(x[1].strip()), float(x[2].strip()), int(x[3].strip()))).toDF()

        # 离线计算时从mysql中加载ratings数据到hive中
        ratings = self.sqlContext.read.format('jdbc') \
            .options(url=self.jdbcURL,
                     driver=self.prop['dirver'],
                     dbtable=self.ratingTable,
                     user=self.prop['user'],
                     password=self.prop['password']).load()

        ratings.write.mode('overwrite').saveAsTable('MovieSizer.ratings')


elt = ELT()
elt.loadLinks2HV()
elt.loadMovies2Hive()
elt.loadTags2Hive()
elt.loadRatings2Hive()

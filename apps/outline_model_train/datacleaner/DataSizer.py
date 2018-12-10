#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: DataSizer.py 
@time: 18-6-25 下午10:05 
"""
from pyspark import SparkConf, SparkContext, SQLContext, HiveContext


class DataSizer:
    def __init__(self):
        self.localClusterURL = "local[2]"
        self.clusterMasterURL = "spark://Master:7077"
        self.conf = SparkConf().setAppName('DaraSizer').setMaster(self.localClusterURL)
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

    def sizerData(self):
        ratings = self.hc.cacheTable('ratings')
        count = self.hc.sql("select count(*) from ratings").first()[0]

        # 将数据分割成训练集和测试集
        percent = 0.6
        trainingDataCount = int((count * percent))
        testDataCount = int(count * (1 - percent))

        # 评分数据按时间升序排列 并根据时间戳去重， 取同一个用户对同一个电影的最近的电影评分
        # trainingDataASC = self.hc.sql('select userId,movieId,rating from ratings order by ts asc')
        trainingDataASC = self.hc.sql(
            'select id, user_id, movie_id, rating, ds from (select *, row_number() over (partition by user_id, movie_id order by ds desc) num from moviesizer.ratings) t where t.num=1 order by ds')
        # trainingDataASC.show()
        trainingDataASC.write.mode('overwrite').saveAsTable('moviesizer.trainingDataASC')

        # 评分数据按时间降序排列
        trainingDataDESC = self.hc.sql(
            'select id, user_id, movie_id, rating, ds from (select *, row_number() over (partition by user_id, movie_id order by ds desc) num from moviesizer.ratings) t where t.num=1 order by ds desc')
        trainingDataDESC.write.mode('overwrite').saveAsTable('moviesizer.trainingDataDESC')

        # 60% 的数据作为训练模型
        trainingData = self.hc.sql('select * from trainingDataAsc limit %d ' % trainingDataCount)
        trainingData.write.mode('overwrite').saveAsTable('moviesizer.trainingData')

        # 40% 作为测试模型
        testData = self.hc.sql('select * from trainingDataDesc limit %d' % testDataCount)
        testData.write.mode('overwrite').saveAsTable('moviesizer.testData')


ds = DataSizer()
ds.sizerData()

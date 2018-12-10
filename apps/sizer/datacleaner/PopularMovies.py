#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
    新用户没有浏览观看记录， 默认推荐播放量前5的电影
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: PopularMovies.py 
@time: 18-6-21 下午9:20 
"""
from pyspark import SparkConf, SparkContext, SQLContext, HiveContext

jdbcURL = "jdbc:mysql://Master:3306/recommend?useUnicode=true&characterEncoding=utf-8&useSSL=false"
alsTable = "recommend.alsTab"
recResultTable = "recommend.similarTab"
top5Table = "recommend.top5Result"
userTable = "recommend.user"
ratingTable = "recommend.rating"
prop = {
    'dirver': 'com.mysql.jdbc.Driver',
    'user': 'root',
    'password': 'woshiwo111'
}


if __name__ == "__main__":
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    conf = SparkConf().setAppName('RecommendForAllUsers').setMaster(clusterMasterURL) \
        .set('spark.executor.memory', '7G')
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    pop = hc.sql("select count(*) as c ,movieId from trainingData group by movieId order by c desc")
    pop.show()
    pop5 = pop.select("movieId").limit(5)
    pop5.show()
    pop5.registerTempTable('pop5')
    pop5Result = hc.sql('select a.movieId,a.title from movies a join pop5 b where a.movieId=b.movieId')
    pop5Result.show()
    pop5Result.write.mode('overwrite').saveAsTable('pop5Result')
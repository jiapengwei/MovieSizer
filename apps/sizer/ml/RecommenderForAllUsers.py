#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: RecommendForAllUsers.py
@time: 18-6-20 下午4:45
"""
from pyspark import SparkConf, SparkContext, SQLContext, HiveContext
from pyspark.mllib.recommendation import MatrixFactorizationModel


jdbcURL = "jdbc:mysql://Master:3306/recommend?useUnicode=true&characterEncoding=utf-8&useSSL=false"
alsTable = "MovieSizer.operation_top5recomm"

prop = {
    'dirver': 'com.mysql.jdbc.Driver',
    'user': 'root',
    'password': 'woshiwo111'
}


class AlsTable:
    def __init__(self, userId: int, movieId: int, rating: float):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating


if __name__ == '__main__':
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    conf = SparkConf().setAppName('RecommendForAllUsers').setMaster(clusterMasterURL) \
        .set('spark.executor.memory', '7G')
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    # users = hc.sql('select distinct(userId) from trainingData order by userId asc')
    # allUsers = users.rdd.map(lambda x: int(x[0])).toLocalIterator()

    dataframe_mysql = sqlContext.read.format("jdbc")\
        .options(url=jdbcURL,
        driver="com.mysql.jdbc.Driver", dbtable="MovieSizer.user_userprofile",
        user="root", password="woshiwo111").load()
    users = dataframe_mysql.select('id')
    users.show()
    allUsers = users.rdd.map(lambda x: int(x[0])).toLocalIterator()
    print(allUsers)
    modelkPath = 'hdfs://Master:9000/tmp/BestModel/0.087178'
    model = MatrixFactorizationModel.load(sc, modelkPath)
    test_tag = 1
    k = 1
    for user in allUsers:
        if test_tag == 1:
            rec = model.recommendProducts(user, 5)
            uidString = list(map(lambda x: str(x.user) + ',' + str(x.product) + ',' + str(x.rating), rec))
            uidDFArray = sc.parallelize(uidString)
            uidDFArray.foreach(print)
            uidDF = uidDFArray.map(lambda x: x.split(',')).map(
                lambda x: (int(x[0]), int(x[1]), float(x[2]))
            ).toDF(['user_id', 'movie_id', 'rating'])
            print('for user %d, top5 recommend' % user)
            uidDF.write.jdbc(url=jdbcURL, table=alsTable, properties=prop, mode='append')
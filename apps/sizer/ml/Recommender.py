#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    为用户产生推荐结果
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Recommender.py 
@time: 18-6-20 下午4:48 
"""
from pyspark import SparkConf, SparkContext, SQLContext, HiveContext
from pyspark.mllib.recommendation import MatrixFactorizationModel

if __name__ == '__main__':
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    conf = SparkConf().setAppName('Recommender').setMaster(clusterMasterURL)\
        .set('spark.executor.memory', '7G')
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    users = hc.sql('select distinct(userId) from trainingData order by userId asc')
    index = 139
    uid = int(users.take(index)[-1][0])
    # print(uid)

    modelPath = '/tmp/BestModel/0.087178'
    model = MatrixFactorizationModel.load(sc, modelPath)
    rec = model.recommendProducts(uid, 5)
    # recmoviesid = rec.map(lambda x: x.product)
    recmoviesid = map(lambda x: x.product, rec)
    print(rec)
    print(recmoviesid)
    print('为用户'+str(uid)+'推荐了以下5部电影：')
    for i in recmoviesid:
        moviename = hc.sql('select title from movies where movieid=%d' % i).first()[0]
        print(str(i) + '  ' + moviename)
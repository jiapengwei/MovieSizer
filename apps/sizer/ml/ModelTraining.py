#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    训练多个模型， 取其中最好， 即取RMSE值最小的模型
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ModelTraining.py 
@time: 18-6-20 下午12:47 
"""
import math
import sys

from pyspark import SparkConf, SQLContext, HiveContext, SparkContext
from pyspark.mllib.recommendation import Rating, ALS

from sizer.conf.AppConf import AppConf


# nohup hive --service metastore > metastore.log 2>&1 &

def main():
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    conf = SparkConf().setAppName('ModelTraining').setMaster(clusterMasterURL) \
        .set('spark.executor.memory', '7G')
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    trainingData = hc.sql('select * from trainingData')
    testData = hc.sql('select * from testData')
    ratingRDD = hc.sql('select * from trainingData').rdd \
        .map(lambda x: Rating(int(x[0]), int(x[1]), float(x[2])))
    training2 = ratingRDD.map(
        lambda x: (x.user, x.product)
    )

    # 测试集， 转换为Rating格式
    testRDD = testData.rdd.map(
        lambda x: Rating(int(x[0]), int(x[1]), float(x[2]))
    )
    # testRDD.foreach(print)
    test2 = testRDD.map(
        lambda x: ((x.user, x.product), x.rating)
    )
    # test2.foreach(print)

    # 特征向量的个数
    rank = 50
    # 正则因子
    lam = [0.001, 0.005, 0.01]
    # 迭代次数
    iteration = [10]  # , 20, 30]
    bestRMSE = sys.float_info.max
    bestIteration = 0
    bestLam = 0.0

    # persist 可以根据情况设置其缓存级别
    ratingRDD.persist()
    training2.persist()
    test2.persist()

    for l in lam:
        for i in iteration:
            model = ALS.train(ratingRDD, rank, i, l)
            predict = model.predictAll(training2).map(
                lambda x: ((x.user, x.product), x.rating)
            )
            # (user, product)为key, 将提供的rating与预测的rating进行比较
            predictAndFact = predict.join(test2)
            MSE = predictAndFact.map(
                lambda x: (x[1][0] - x[1][1]) * (x[1][0] - x[1][1])
            ).mean()
            RMSE = math.sqrt(MSE)
            if RMSE < bestRMSE:
                model.save(sc, '/tmp/BestModel/%lf' % RMSE)
                bestRMSE = RMSE
                bestIteration = i
                bestLam = l

            print('Best model is located in /tmp/BestModel/%lf' % RMSE)
            print("Best RMSE is %lf" % RMSE)
            print("Best Iteration is %d" % bestIteration)
            print("Best Lambda is %lf" % bestLam)


if __name__ == '__main__':
    main()

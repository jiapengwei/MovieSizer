#!/usr/bin/python
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ItemSimilarity.py 
@time: 18-6-22 下午3:57 
"""
from math import sqrt

from sizer.caseclass.ItemSimi import ItemSimi


def similarity(user_rdd, stype):
    """
        相似度计算
    :param user_rdd:    RDD[ItemPref]  用户评分数据
    :param stype:       string         相似度计算类型
    :return:
    """
    if stype == 'coocurrence':
        return cooccurrenceSimilarity(user_rdd)
    elif stype == 'cosine':
        return cosineSimilarity(user_rdd)
    elif stype == 'euclidean':
        return euclideanDistanceSimilarity(user_rdd)
    else:
        return cooccurrenceSimilarity(user_rdd)


def cooccurrenceSimilarity(user_rdd):
    """
        同现实现用户相似度矩阵计算
        w(i, j) = N(i) n N(j) / sqrt(N(i) * M(i))
    :param user_rdd: 用户评分(ItemPref)
    :return:
    """

    user_rdd1 = user_rdd.map(lambda x: (x.userId, x.movieId, x.rating))
    user_rdd2 = user_rdd1.map(lambda x: (x[0], x[1]))
    # 1(用户： 物品) 笛卡尔积 （用户： 物品） => (物品： 物品)
    user_rdd3 = user_rdd2.join(user_rdd1)
    user_rdd4 = user_rdd3.map(lambda x: (x[1], 1))
    # 2 物品： 物品： 频次
    user_rdd5 = user_rdd4.reduceByKey(lambda x, y: x + y)
    # 3 对角矩阵
    user_rdd6 = user_rdd5.filter(lambda x: x[0][0] == x[0][1])
    # 4 非对角矩阵
    user_rdd7 = user_rdd5.filter(lambda x: x[0][0] != x[0][1])
    # 5 计算同现相似度（ 物品1， 物品2， 同现频次）
    user_rdd8 = user_rdd7.map(
        lambda x: (x[0][0], (x[0][0], x[0][1], x[1]))
    ).join(user_rdd6.map(lambda x: (x[0][1], x[1])))
    user_rdd9 = user_rdd8.map(
        lambda x: (x[1][0][1], (x[1][0][0], x[1][0][1], x[1][0][2], x[1][1]))
    )
    user_rdd10 = user_rdd9.join(user_rdd6.map(
        lambda x: (x[0][0], x[1])
    ))
    user_rdd11 = user_rdd10.map(
        lambda x: (x[1][0][0], x[1][0][1], x[1][0][2], x[1][0][3], x[1][1])
    )
    user_rdd12 = user_rdd11.map(
        lambda x: (x[0], x[1], (x[2] / sqrt(x[3] * x[4])))
    )

    return user_rdd12.map(
        lambda x: (x[0], x[1], x[2])
    ).filter(lambda x: x[2] >= 0.4)

def cosineSimilarity(user_rdd):
    """
        同现实现用户相似度矩阵计算
        w(i, j) = N(i) n N(j) / sqrt(N(i) * M(i))
    :param user_rdd: 用户评分(ItemPref)
    :return:
    """


def euclideanDistanceSimilarity(user_rdd):
    """
        同现实现用户相似度矩阵计算
        w(i, j) = N(i) n N(j) / sqrt(N(i) * M(i))
    :param user_rdd: 用户评分(ItemPref)
    :return:
    """
    pass

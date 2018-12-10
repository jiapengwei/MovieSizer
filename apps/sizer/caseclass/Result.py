#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    存放推荐结果
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm
@file: Result.py 
@time: 18-6-19 下午11:07 
"""


class Result:
    def __init__(self, userId: int, movieId: int, rating: float):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating

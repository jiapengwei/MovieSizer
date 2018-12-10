#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    用于描述信息的样例类
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Ratings.py 
@time: 18-6-19 下午11:05 
"""


class Ratings:
    def __init__(self, userId: int, movieId: int, rating: float, ts: int):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.ts = ts

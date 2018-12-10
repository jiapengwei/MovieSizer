#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    接收用户的评分信息
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: UserRating.py 
@time: 18-6-19 下午11:15 
"""


class UserRating:
    def __init__(self, userId: int, movieId: int, rating: float):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating

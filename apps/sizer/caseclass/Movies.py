#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    用于描述信息的样例类
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Movies.py 
@time: 18-6-19 下午11:03 
"""
import string


class Movies:
    def __init__(self, movieId: int, title: string, genres: string):
        self.movieId = movieId
        self.title = title
        self.genres = genres

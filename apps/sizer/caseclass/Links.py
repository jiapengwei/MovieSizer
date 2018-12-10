#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    用于描述信息的样例类
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Links.py
@time: 18-6-19 下午10:59 
"""


class Links:
    def __init__(self, movieId: int, imdbId: int, tmdbId: int):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId

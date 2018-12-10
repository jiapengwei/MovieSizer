#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    用于描述信息的样例类
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Tags.py 
@time: 18-6-19 下午11:11 
"""
import string


class Tags:
    def __init__(self, userId: int, movieId: int, tag: string, ts: int):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.ts = ts

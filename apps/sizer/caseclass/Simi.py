#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    存放物品相似度
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Simi.py 
@time: 18-6-19 下午11:09 
"""


class Simi:
    def __init__(self, itemId1: int, itemId2: int, similar: float):
        self.itemId1 = itemId1
        self.itemId2 = itemId2
        self.similar = similar

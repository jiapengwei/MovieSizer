#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ItemSimi.py 
@time: 18-6-22 下午4:19 
"""

from pyspark.serializers import Serializer


class ItemSimi(Serializer):
    """
        相似度
    """

    def __init__(self, item1, item2, similar):
        self.item1 = item1
        self.item2 = item2
        self.similar = similar

#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ItemPref.py 
@time: 18-6-22 下午4:19 
"""


class ItemPref:
    """
        用户评分
    """

    def __init__(self, userid, itemid, pref):
        self.userid = userid
        self.itemid = itemid
        self.pref = pref

#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: Users.py 
@time: 18-6-19 下午11:16 
"""
import string


class Users:
    def __init__(self, userId: int, gender: string, age: int, occupation: int):
        self.userId = userId
        self.gender = gender
        self.age = age
        self.occupation = occupation

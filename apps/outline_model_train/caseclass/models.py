#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: models.py 
@time: 18-6-25 下午2:56 
"""
import string


class Link:
    def __init__(self, movieId: int, imdbId: int, tmdbId: int):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId


class Movie:
    def __init__(self, movieId: int, title: string, genres: string):
        self.movieId = movieId
        self.title = title
        self.genres = genres


class Rating:
    def __init__(self, userId: int, movieId: int, rating: float, ts: int):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.ts = ts


class Tag:
    def __init__(self, userId: int, movieId: int, tag: string, ts: int):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.ts = ts


class ItemPref:
    """
        用户评分
    """

    def __init__(self, userid, itemid, pref):
        self.userid = userid
        self.itemid = itemid
        self.pref = pref


class ItemSimi:
    """
        相似度
    """

    def __init__(self, item1, item2, similar):
        self.item1 = item1
        self.item2 = item2
        self.similar = similar


class Result:
    def __init__(self, userId: int, movieId: int, rating: float):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating


class Similarity:
    def __init__(self, itemId1: int, itemId2: int, similar: float):
        self.itemId1 = itemId1
        self.itemId2 = itemId2
        self.similar = similar

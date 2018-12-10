#!/usr/bin/python
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: adminx.py 
@time: 18-6-21 下午6:25 
"""
import xadmin

from operation.models import Brow, Review, Rating, Default5Recommend, Top5Recommend


class BrowAdmin(object):
    # 列表默认显示
    list_display = ['id', 'user', 'movie', 'browtime']
    # 搜索范围
    search_fields = ['id', 'user', 'movie']
    # 列表过滤
    list_filter = ['id', 'user', 'movie', 'browtime']
    # 只读
    # readonly_fields = []
    # 直接编辑
    list_editable = ['user', 'movie']
    # 默认排序
    ordering = ['id', 'user', 'movie', 'browtime']


class ReviewAdmin(object):
    list_display = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
    search_fields = ['id', 'user', 'movie', 'content', 'star']
    list_filter = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']
    list_editable = ['user', 'movie', 'content', 'star']
    ordering = ['id', 'user', 'movie', 'content', 'star', 'reviewtime']


class Default5RecommendAdmin(object):
    # list_display = ['id', 'movie', 'retime']
    # search_fields = ['id', 'movie']
    # list_filter = ['id', 'movie', 'retime']
    # ordering = ['id', 'movie']
    list_display = ['id', 'movie', 'redate']
    search_fields = ['id', 'movie']
    list_filter = ['id', 'movie', 'redate']
    ordering = ['id', 'movie', 'redate']


class Top5RecommendAdmin(object):
    list_display = ['id', 'user', 'movie']
    search_fields = ['id', 'userid', 'movie']
    list_filter = ['id', 'user', 'movie']
    ordering = ['id', 'user', 'movie']


# class Rating(models.Model):
#     RATING_RANGE = (
#         MaxValueValidator(5),
#         MinValueValidator(0)
#     )
#     movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
#     user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
#     rating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
#     ds = models.BigIntegerField(default=

class RatingAdmin(object):
    list_display = ['id', 'movie', 'user', 'rating', 'ds']
    search_fields = ['id', 'movie', 'user', 'rating', 'ds']
    list_filter = ['id', 'movie', 'user', 'rating', 'ds']
    ordering = ['id', 'movie', 'user', 'rating', 'ds']


xadmin.site.register(Brow, BrowAdmin)
xadmin.site.register(Review, ReviewAdmin)
xadmin.site.register(Default5Recommend, Default5RecommendAdmin)
xadmin.site.register(Top5Recommend, Top5RecommendAdmin)
xadmin.site.register(Rating, RatingAdmin)
#

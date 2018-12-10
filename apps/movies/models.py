import datetime
import time

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from user.models import UserProfile


class MovieCategory(models.Model):
    category = models.CharField(max_length=100, default='', verbose_name='电影类型')
    movienum = models.IntegerField(default=0, verbose_name='电影数量')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = '电影类型'
        verbose_name_plural = verbose_name


class MovieInfo(models.Model):
    RATING_RANGE = (
        MaxValueValidator(5),
        MinValueValidator(0)
    )
    # moviename = models.CharField(max_length=1000, default='', verbose_name='电影名称')
    # showyear = models.DateField(default=datetime.now, verbose_name='上映年份', null=True, blank=True)
    # nation = models.CharField(max_length=255, default='', verbose_name='国家', null=True, blank=True)
    # director = models.CharField(max_length=1000, default='', verbose_name='导演', null=True, blank=True)
    # leadactors = models.CharField(max_length=1000, default='', verbose_name='主演', null=True, blank=True)
    # screenwriter = models.CharField(max_length=255, default='', verbose_name='编剧', null=True, blank=True)
    # picture = models.URLField(max_length=1000, verbose_name='海报', null=True, blank=True)
    # averating = models.FloatField(default='', validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
    # numrating = models.IntegerField( default=0, verbose_name='评分人数', null=True, blank=True)
    # description = models.CharField(max_length=1000, default='', verbose_name='简介', null=True, blank=True)
    # typelist = models.CharField(max_length=255, default='', verbose_name='类型', null=True, blank=True)
    # backpost = models.CharField(max_length=15000, default='', null=True, blank=True)
    moviename = models.CharField(max_length=1000, default='', verbose_name='电影名称')
    # showyear = models.CharField(max_length=10, verbose_name='上映年份', null=True, blank=True)
    releasedate = models.DateField(default=datetime.datetime.now, verbose_name='上映年份', null=True, blank=True)
    nation = models.CharField(max_length=255, default='', verbose_name='国家', null=True, blank=True)
    directors = models.CharField(max_length=1000, default='', verbose_name='导演', null=True, blank=True)
    leadactors = models.CharField(max_length=1000, default='', verbose_name='主演', null=True, blank=True)
    editors = models.CharField(max_length=255, default='', verbose_name='编剧', null=True, blank=True)
    picture = models.URLField(max_length=1000, verbose_name='海报', null=True, blank=True,default='/static/images/t3.jpg')
    averating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
    numrating = models.IntegerField(default=0, verbose_name='评分人数', null=True, blank=True)
    description = models.TextField(default='', verbose_name='简介', null=True, blank=True)
    typelist = models.ManyToManyField(MovieCategory, verbose_name='类型')
    backpost = models.CharField(max_length=3000, default='', null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.directors, self.moviename)

    class Meta:
        verbose_name = '电影信息'
        verbose_name_plural = verbose_name


class MovieSimilar(models.Model):
    item1 = models.IntegerField(default=0, verbose_name='电影id')
    item2 = models.IntegerField(default=0, verbose_name='电影id')

    # item1 = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    # item2 = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    similar = models.FloatField(default=0, verbose_name='相似度')

    def __str__(self):
        return '%d - %d - %lf' % (self.item1, self.item2, self.similar)

    class Meta:
        verbose_name = '电影相似度信息'
        verbose_name_plural = verbose_name






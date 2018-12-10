import time
import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from movies.models import MovieInfo
from user.models import UserProfile


class Brow(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    browtime = models.DateTimeField(default=datetime.datetime.now, verbose_name='浏览时间')

    def __str__(self):
        return '%s - %s - %s' % (self.user.username, self.movie.moviename, self.browtime)

    class Meta:
        verbose_name = '浏览信息'
        verbose_name_plural = verbose_name


class Review(models.Model):
    STAR_RANGE = [
        MaxValueValidator(5),
        MinValueValidator(0)
    ]
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    content = models.TextField(max_length=255, default='', verbose_name='评论', null=True, blank=True)
    star = models.FloatField(default=0, validators=STAR_RANGE, verbose_name='星级')
    reviewtime = models.DateTimeField(default=datetime.datetime.now, verbose_name='提交时间')

    def __str__(self):
        return '%s - %s - %lf' % (self.user.username, self.movie.moviename, self.star)

    class Meta:
        verbose_name = '用户回执'
        verbose_name_plural = verbose_name


class Default5Recommend(models.Model):
    movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    # movie = models.IntegerField(default=0, verbose_name='电影id')
    redate = models.DateField(default=datetime.datetime.now, verbose_name='推荐时间')

    def __str__(self):
        return str(self.movie_id)

    class Meta:
        verbose_name = '默认电影推荐'
        verbose_name_plural = verbose_name


class Top5Recommend(models.Model):
    # movieid = models.IntegerField(default=0, verbose_name='电影id')
    # userid = models.IntegerField(default=0, verbose_name='用户id')
    movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    rating = models.FloatField(default=0, verbose_name='评分')

    def __str__(self):
        return '%s - %s -%lf' % (self.user, self.movie, self.rating)
        # return '%s - %s -%lf' % (self.userid, self.movieid, self.rating)

    class Meta:
        verbose_name = '用户推荐信息'
        verbose_name_plural = verbose_name


class Rating(models.Model):
    RATING_RANGE = (
        MaxValueValidator(5),
        MinValueValidator(0)
    )
    movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    rating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)
    ds = models.BigIntegerField(default=time.mktime(datetime.datetime.now().timetuple()), verbose_name='时间戳')

    def __str__(self):
        return '%s - %s - %lf' % (self.user, self.movie, self.rating)

    class Meta:
        verbose_name = '用户评分'
        verbose_name_plural = '用户评分'


class AlsTable(models.Model):
    RATING_RANGE = (
        MaxValueValidator(5),
        MinValueValidator(0)
    )
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieInfo, verbose_name='电影', on_delete=models.CASCADE)
    rating = models.FloatField(default=0, validators=RATING_RANGE, verbose_name='评分', null=True, blank=True)

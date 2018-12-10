#!/usr/bin/python  
# -*- coding:utf-8 _*-
"""
    用于原始的数据清洗
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: ELT.py 
@time: 18-6-19 下午9:57
"""
import os

from pyspark import SparkContext, SparkConf, SQLContext, HiveContext

# tags中大部分数据格式如下：
#    4208,260,Action-packed,1438012536
# 但会出现如下的数据：
#    4208,260,"Family,Action-packed",1438012562
# 这样对数据split后插入hive中就会出错,需清洗数据：
#    4208,260,"Family,Action-packed",1438012562 => 4208,260,FamilyAction-packed,1438012562
from sizer.caseclass.Links import Links
from sizer.caseclass.Movies import Movies
from sizer.caseclass.Ratings import Ratings
from sizer.caseclass.Tags import Tags


def rebuild(inStr):
    # return inStr.strip().replace('"', '')
    a = inStr.split(',')
    head = ','.join(a[:2])
    tail = str(a[-1])
    a.pop()
    a.pop(0)
    a.pop(0)
    bo = ' '.join(a).replace('"', '').replace("'", '')
    return head + ',' + bo + ',' + tail

def rebuild_mo(inStr):
    a = inStr.split(',')
    head = a[0]
    tail = a[-1]
    a.pop()
    a.pop(0)
    bo = ' '.join(a).replace('"', '').replace("'", '').replace(',', ' ')
    return head + ',' + bo + ',' + tail

# sizertest = "122892,Avengers: Age of Ultron (2015),Action|Adventure|Sci-Fi"
# print(rebuild_mo(sizertest))

if __name__ == '__main__':
    localClusterURL = "local[2]"
    clusterMasterURL = "spark://Master:7077"
    print(os.environ['SPARK_HOME'])
    print(os.environ['HADOOP_HOME'])
    conf = SparkConf().setAppName("ELT").setMaster(localClusterURL)
    sc = SparkContext.getOrCreate(conf)
    sqlContext = SQLContext(sc)
    hc = HiveContext(sc)

    # 设置RDD的partition的数量一般以集群分配给应用的CPU核数的整数倍为宜。
    minPartitions = 8

    # spark -submit --class com.sizer.datacleaner.ETL lib / Spark_Movie.jar
    # 通过case class来定义Links的数据结构，数据的schema，适用于schama已知的数据
    # 也可以通过StructType的方式，适用于schema未知的数据，具体参考文档：
    # http://spark.apache.org/docs/1.6.2/sql-programming-guide.html
    # programmatically-specifying-the-schema

    links = sc.textFile('hdfs://Master:9000/movie/data/links.txt', minPartitions).filter(lambda x: not x.endswith(','))\
        .map(lambda x: x.split(',')).map(lambda x: Links(int(x[0].strip()), int(x[1].strip()), int(x[2].strip()))).toDF()
    movies = sc.textFile('hdfs://Master:9000/movie/data/movies.txt', minPartitions).filter(lambda x: not x.endswith(','))\
        .map(lambda x: rebuild_mo(x)).map(lambda x: x.split(',')).map(lambda x: Movies(int(x[0]), str(x[1]), str(x[2]))).toDF()
    ratings = sc.textFile('hdfs://Master:9000/movie/data/ratings.txt', minPartitions).filter(lambda x: not x.endswith(','))\
        .map(lambda x: x.split(',')).map(lambda x: Ratings(int(x[0].strip()), int(x[1].strip()), float(x[2].strip()), int(x[3].strip()))).toDF()
    tags = sc.textFile('hdfs://Master:9000/movie/data/tags.txt', minPartitions).filter(lambda x: not x.endswith(','))\
        .map(lambda x: rebuild(x)).map(lambda x: x.split(',')).map(lambda x: Tags(int(x[0].strip()), int(x[1].strip()), str(x[2].strip()), int(x[3].strip()))).toDF()

    # 通过数据写入到HDFS，将表存到hive中
    # links
    links.write.mode('overwrite').saveAsTable('links')
    # links.write.mode('overwrite').parquet("/tmp/links")
    # hc.sql("drop table if exists links")
    # hc.sql("create table if not exists links(movieId BIGINT,imdbId BIGINT,tmdbId BIGINT) stored as parquet")
    # hc.sql("load data inpath '/tmp/links' into table links")

    # movies
    movies.write.mode('overwrite').saveAsTable('movies')
    # movies.write.mode('overwrite').parquet("/tmp/movies")
    # hc.sql("drop table if exists movies")
    # hc.sql("create table if not exists movies(movieId BIGINT,title string,genres string) stored as parquet")
    # hc.sql("load data inpath '/tmp/movies' into table movies")

    # ratings
    ratings.write.mode('overwrite').saveAsTable('ratings')
    # ratings.write.mode('overwrite').parquet("/tmp/ratings")
    # hc.sql("drop table if exists ratings")
    # hc.sql("create table if not exists ratings(userId BIGINT,movieId BIGINT,rating double,ts BIGINT) stored as parquet")
    # hc.sql("load data inpath '/tmp/ratings' into table ratings")

    # tags
    tags.write.mode('overwrite').saveAsTable('tags')
    # tags.write.mode('overwrite').parquet("/tmp/tags")
    # hc.sql("drop table if exists tags")
    # hc.sql("create table if not exists tags(userId BIGINT,movieId BIGINT,tag string,ts BIGINT) stored as parquet")
    # hc.sql("load data inpath '/tmp/tags' into table tags")

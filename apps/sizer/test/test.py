#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: test.py 
@time: 18-6-20 下午10:29 
"""

from pyspark import SparkContext
from pyspark.sql import SQLContext
import sys

# solve the UnicodeEncodeError

if __name__ == "__main__":
    sc = SparkContext(appName="mysqltest")
    sqlContext = SQLContext(sc)
    df = sqlContext.read.format("jdbc").options(url="jdbc:mysql://localhost\
    :3306/logstat?user=root&password=woshiwo111", dbtable="lms_levels").load()
    df.show()
    sc.stop()
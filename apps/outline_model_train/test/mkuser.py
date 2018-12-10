#!/usr/bin/python  
# -*- coding:utf-8 _*-
""" 
@author: Sizer
@contact: 591207060@qq.com 
@software: PyCharm 
@file: mkuser.py 
@time: 18-6-25 下午8:26 
"""

import pymysql

if __name__ == "__main__":
    db = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='woshiwo111',
        db='MovieSizer',
        charset="utf8")

    # 获取游标对象
    cursor = db.cursor()

    # for id in range(3, 672):
    #     print(id)
    #     cursor.execute('insert into user_userprofile(id, password, username, is_staff, is_active, is_superuser, date_joined, nick_name, first_name, last_name, email, gender) value("%d", "woshiwo111", "%s", 1, 1, 0, "2018-6-24", "%s", "first_name", "last_name", "123@admin.com", "male");' % (id, "user"+str(id), "user"+str(id)))
    #     db.commit()

    for id in range(1, 185589):
        cursor.execute('select id, moviename from movies_movieinfo where id=%d' % id)
        result = cursor.fetchall()
        print(id, end=' :')
        if not result:
            cursor.execute('insert into movies_movieinfo(id, moviename) values ("%d", "%s")' % (id, "testMovie"+str(id)))
            db.commit()
        else:
            print('%s' % result[0][1])
# -*- coding:utf-8 _*-
from imdb import IMDb
import pymysql
ia = IMDb()
file_path = '/home/sizer/下载/ml-latest-small/links.txt'
i = 0
db = pymysql.connect('localhost', 'root', 'woshiwo111', 'MovieSizer', charset='utf8')
cursor = db.cursor()
# with open(file_path) as f:
#     for line in f.readlines():
#         if i < 1:
#             ah = line.split(',')
#             imdbid, id = ah[1], ah[0]
#             print(line)
#
#             reponse = ia.get_movie(imdbid)
#             moviename = reponse['title'].replace('"', "'")
#             showyear = reponse['year']
#             nation = '|'.join(reponse['countries']).replace('"', "'")
#             director = '|'.join(list(map(lambda x: x['name'].replace('"', "'"), reponse['directors']))[:10])
#             leadactors = '|'.join(list(map(lambda x: x['name'].replace('"', "'"), reponse['cast']))[:10])
#             editors = '|'.join(list(map(lambda x: x['name'].replace('"', "'"), reponse['editors']))[:10])
#             # editors = ''
#             picture = reponse['cover url']
#             averating = float(reponse['rating'])
#             numrating = int(reponse['votes'])
#             description = reponse['plot outline_model_train'].replace('"', "'")
#             typelist = '|'.join(reponse['genres']).replace('"', "'")
#             # backpost =
#             # print('%s, %s, %s' % (imdbid, moviename, showyear))
#             sql = "INSERT INTO movies_movieinfo" \
#                   "(id, moviename, showyear, nation, director, leadactors, editors, picture, averating, numrating, description)" \
#                   ' values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%lf", %d, "%s");' % (id, moviename, showyear, nation, director, leadactors, editors, picture, averating, numrating, description)
#             print(sql)
#             try:
#                 cursor.execute(sql)
#             except:
#                 print('not success !, %s' % id)
#                 db.commit()
#             # i += 1
#         else:
#             break
# db.close()
the_matrix = ia.get_movie('0116839')
k = ia._get_infoset()
print(the_matrix)
print(type(the_matrix))
print(str(the_matrix['director']))
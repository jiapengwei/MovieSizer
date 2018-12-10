from django.http import HttpResponseRedirect
from django.shortcuts import render

from operation.models import Top5Recommend
from operation.views import recommendForUser
from .models import MovieInfo, MovieSimilar
# Create your views here.
from django.views import View
from operation.models import Review
from django.http import HttpResponse
class ContentView(View):
    def get(self, request, movie_id):
        # # all_movieinfo = MovieInfo.objects.get(id=int(movie_id))
        # # all_movie = all_movieinfo.objects.all();
        # # print(all_movie.name)
        # movieinfo = MovieInfo.objects.get(id=movie_id)
        #
        # similar_movies_id = MovieSimilar.objects.all()
        movieinfo = MovieInfo.objects.get(id=movie_id)
        # 对用户进行的个性化推荐
        user_recommend_movies = recommendForUser(request)
        # 相似电影
        similar_movies_ids = MovieSimilar.objects.filter(item1=movie_id).order_by('-similar')[:10]
        # similar_movies = list(map(lambda x: MovieInfo.objects.get(x.movie_id), similar_movies))
        similar_movies = list(map(lambda x: MovieInfo.objects.get(id=x.item2), similar_movies_ids))
        all_comments = Review.objects.all()
        # all_movieinfo = MovieInfo.objects.all()
        # movielaster = all_movieinfo[0:2]
        return render(request, 'content.html', {"movieinfo": movieinfo,
                                                # "movielaster": movielaster,
                                                "similar_movies": similar_movies,
                                                "recommend_movies": user_recommend_movies,
                                                "all_comments":all_comments})

class AddComment(View):
    # 用户添加用户评论
    def post(self,request):
        # if not request.user.is_authenticated:
        #     return HttpResponse('{"status":"fail",",msg":"用户未登陆"}',content_type='application/json')
        movie_id = request.POST.get("movie_id", '0')
        comments = request.POST.get("comments", "")
        if int(movie_id) > int(0) and comments:
            movie_comments = Review()
            movie = MovieInfo.objects.get(id=movie_id)
            movie_comments.movie = movie
            movie_comments.content = comments
            movie_comments.user = request.user
            # movie_comments.user_id = 1
            # movie_comments.movie_id = 2
            # movie_comments.content = 'hello'
            # movie_comments.star = 3.0
            movie_comments.save()
            return HttpResponse('{"status":"success",",msg":"添加成功"}', content_type='application/json')
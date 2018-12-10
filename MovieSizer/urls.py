"""MovieSizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path
from django.conf.urls import url
from operation.views import IndexView
from user.views import LoginView, LogoutView
from movies.views import ContentView,AddComment
from user.views import RegisterView
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # 首页
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('content/', ContentView.as_view(), name="content",),
    path('register/', RegisterView.as_view(), name="register",),
    path('movieinfo/<int:movie_id>', ContentView.as_view(), name='movieinfo'),
    path('add_comment/', AddComment.as_view(), name='addcomments')
]

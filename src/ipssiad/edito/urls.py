from django.urls import path, re_path
from . import views

app_name = 'edito'

urlpatterns = [
    path('articles/', views.articles , name='articles'),
    re_path('articles/(?P<uuid>[\w-]+)/$', views.article , name='article'),
]

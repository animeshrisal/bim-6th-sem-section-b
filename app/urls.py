from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('movies/', views.get_movies),
    path('movies/<int:id>/', views.get_movie),
    path('post_movie/', views.post_movie)
]
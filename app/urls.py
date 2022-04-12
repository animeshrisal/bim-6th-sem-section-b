from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('movies/', views.get_movies),
    path('movies/<int:id>/', views.get_movie),
    path('post_movie/', views.post_movie),
    path('signup/', views.signup),
    path('signin/', views.signin),
    path('signout/', views.signout),
    path('add_to_favorite/<int:id>', 
            views.add_to_favorite, 
            name="Add to favorite"),
    path('remove_from_favorites/<int:id>',
            views.remove_from_favorites, 
            name="Remove from favorite"),

    path('user_favorites/', 
            views.get_user_favorites),

    path('search_movies/', views.search_movies) 
   
]
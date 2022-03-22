from django.shortcuts import redirect, render

from app.forms import MovieForm
from .models import Movie

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Create your views here.
def about(request):
    return render(request, 'about.html')

def get_movies(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html',
     {'movies': movies})

def get_movie(request, id):
    movie = Movie.objects.get(pk=id)
    return render(request, 'movie.html', {'movie': movie})

def post_movie(request):
    movie_form = MovieForm()
    
    if request.method == "POST":
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()

            return redirect('/movies/')

    return render(request, 'post_movie.html', {'movie_form': movie_form})


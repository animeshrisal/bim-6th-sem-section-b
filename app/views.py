from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .forms import MovieForm, ReviewForm
from .models import Movie, Review

from django.core.paginator import Paginator
# Create your views here.
def index(request):
    return render(request, 'index.html')

# Create your views here.
def about(request):
    return render(request, 'about.html')

def get_movies(request):
    movies = Movie.objects.all()

    paginator = Paginator(movies, 5) # Show 5 contacts per page.

    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    return render(request, 'movies.html',
     {'movies': movies})

def get_movie(request, id):
    try:
        review_form = ReviewForm()
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.movie_id = id
                review.user_id = request.user.id
                review.save()

        movie = Movie.objects.get(pk=id)

        context = {
            'is_favorite': False
        }

        if movie.favorite.filter(pk=request.user.pk).exists():
            context['is_favorite'] = True

        reviews = Review.objects.filter(
            movie=movie
        ).order_by('-created_at')[0:4]
        
        return render(request, 'movie.html', {'movie': movie,             
            'reviews': reviews,
            'review_form': review_form,
            'context': context
            })
            
    except Movie.DoesNotExist:
        return render(request, '404.html')


def post_movie(request):
    movie_form = MovieForm() 
    if request.method == "POST":
        movie_form = MovieForm(request.POST)

        if movie_form.is_valid():
            movie_form.save()
            return redirect('/movies/')

    return render(request, 'post_movie.html',
     {'movie_form': movie_form})


def signin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password'])
            login(request, user)
            return redirect('/movies/')

    return render(request, 'signin.html', {'form': form})

def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/movies/')

    return render(request, 'signup.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/movies/')

def add_to_favorite(request, id):
    movie = Movie.objects.get(id=id)
    movie.favorite.add(request.user)

    return redirect('/movies/{0}'.format(id))

def remove_from_favorites(request, id):
    movie = Movie.objects.get(id=id)
    movie.favorite.remove(request.user)

    return redirect('/movies/{0}'.format(id))

def get_user_favorites(request):
    movies = request.user.favorite.all()
    return render(request, 'user_favorite.html', {'movies': movies})

def search_movies(request):
    search_term = request.GET.get('search', '')
    if search_term != '':
        movies = Movie.objects.filter(title__contains=search_term)
    else:
        movies = []
    return render(request, 'search.html', 
    {'movies': movies, 'search_term': search_term})

    
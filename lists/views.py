from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from classes import KP_Movie


# Create your views here.
@api_view()
def response_check(request):
    return Response(data={'message': 'alive'})


@api_view(['GET'])
def view_movies(request):
    return render(request, 'lists/index.html')


@api_view(['GET'])
def view_archive_movies(request):
    return render(request, 'lists/index.html', context={'archive': True})


@api_view(['GET', 'POST'])
def add_movie(request):
    if request.method == 'GET':
        return render(request, 'lists/addMovie.html')

    kp = KP_Movie()
    movie = kp.get_movie_by_id(request.movie_id)
    return Response(data={'status': True, 'error': '', 'dt': request.movie_id})


@api_view(['GET'])
def movies_dump(request):
    movies_file = 'data/movies_to_watch_old.json'
    archive_movies_file = 'data/archive_movies_old.json'
    file_name = archive_movies_file if request.query_params.get('archive') else movies_file
    with open(file_name, 'r') as f:
        movies = json.load(f)
    return Response(movies)

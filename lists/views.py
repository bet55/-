from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from classes import KP_Movie
from lists.serializers import FilmSerializer, GenreSerializer
from utils import convert_file
from lists.models import Film


# Create your views here.
@api_view()
def response_check(request):
    return Response(data={'message': 'alive'})


@api_view()
def view_postcard(request):
    return render(request, 'lists/postcard.html')


@api_view(['GET'])
def view_movies(request):
    response_format = request.query_params.get('format', 'html')
    is_archive = 'archive' in request.path
    film = Film._film_manager.filter(is_archive=is_archive).order_by('-rating_kp').values()
    serialize = FilmSerializer(film, many=True)

    # return Response({'test': response_format == 'json'})

    if response_format == 'json':
        return Response(serialize.data)

    return render(request, 'lists/movies.html', context={'data': serialize.data})


@api_view(['GET'])
def view_movie_by_id(request, kp_id):
    film = Film._film_manager.filter(kp_id=kp_id)
    serialize = FilmSerializer(film)

    return Response(serialize.data)


@api_view(['GET', 'POST'])
def add_movie(request):
    if request.method == 'GET':
        return render(request, 'lists/add_movie.html')

    kp = KP_Movie()
    kp_movie = kp.get_movie_by_id(request.movie_id)

    return Response(data={'status': True, 'error': '', 'dt': request.movie_id})


@api_view(['GET'])
def view_movies_old_format(request):
    movies_file = 'data/movies_to_watch_old.json'
    archive_movies_file = 'data/archive_movies_old.json'
    file_name = archive_movies_file if request.query_params.get('archive') else movies_file
    with open(file_name, 'r') as f:
        movies = json.load(f)
    return Response(movies)


@api_view(['GET'])
def save_movies_to_db(request):
    movies_json = 'data/movies_to_watch_dump.json'
    archive_movies_json = 'data/archive_movies_dump.json'

    failed_movies_file = 'data/failed_movies.json'
    error_file = 'data/save_error.json'

    is_archive = bool(request.query_params.get('archive'))
    json_file = archive_movies_json if is_archive else movies_json

    count = convert_file(json_file, failed_movies_file, error_file, is_archive)
    return Response({'saved_count': count})

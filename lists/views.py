from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import json

from rest_framework.views import APIView

from classes import KP_Movie
from lists import serializers
from lists.models import Film, Director, Genre, Actor, Writer
from utils import convert_movie_info, convert_file
from lists.serializers import FilmSerializer, GenreSerializer
from utils import convert_file
from lists.models import Film


# Create your views here.
class ToWatchList(APIView):
    def get(self, request):
        queryset = Film._film_manager.all().filter(is_archive=False).order_by('-rating_kp')
        serializer = serializers.FilmSmallSerializer(queryset, many=True)
        return render(request, 'lists/movies.html', context={'data': serializer.data})


class ArchiveList(APIView):
    def get(self, request):
        queryset = Film._film_manager.all().filter(is_archive=True).order_by('-rating_kp')
        serializer = serializers.FilmSmallSerializer(queryset, many=True)
        return render(request, 'lists/movies.html', context={'data': serializer.data})


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


@api_view(['GET'])
def do_shit(request):
    file_path = 'data/api_response.json'
    with open(file_path, 'r') as f:
        data = json.load(f)
    film = Film()
    if data.get('id') and data.get('name'):
        film.kp_id = data.get('id')
        film.name = data.get('name')
    else:
        return Response('No kp_id or name')
    if data.get('countries'):
        film.countries = [country.get('name', 'unknown') for country in data.get('countries')]
    if data.get('budget', {}).get('value'):
        film.budget = data.get('budget').get('value')
    if data.get('fees', {}).get('world', {}).get('value'):
        film.fees = data.get('fees').get('world').get('value')
    if data.get('premiere', {}).get('world'):
        film.premiere = data.get('premiere').get('world')
    if data.get('description'):
        film.description = data.get('description')
    if data.get('short_description'):
        film.short_description = data.get('short_description')
    if data.get('slogan'):
        film.slogan = data.get('slogan')
    if data.get('duration'):
        film.duration = data.get('duration')
    if data.get('poster', {}).get('url'):
        film.poster = data.get('poster').get('url')
    if data.get('rating', {}).get('kp'):
        film.rating_kp = data.get('rating').get('kp')
    if data.get('rating', {}).get('imdb'):
        film.rating_imdb = data.get('rating').get('imdb')
    if data.get('votes', {}).get('kp'):
        film.votes_kp = data.get('votes').get('kp')
    if data.get('votes', {}).get('imdb'):
        film.votes_imdb = data.get('votes').get('imdb')
    film.save()
    if data.get('genres'):
        for g in data.get('genres'):
            genre, _ = Genre._genre_manager.update_or_create(name=g.get('name'))
            film.genres.add(genre)
    if data.get('persons'):
        valid_person = [person for person in data.get('persons') if
                           (person.get('enProfession') == 'director' and
                            person.get('name') is not None and
                            person.get('id') is not None)]
        for p in valid_person:
            person, _ = Director._director_manager.update_or_create(name=p.get('name'),
                                                                    kp_id=p.get('id'),
                                                                    photo=p.get('photo'))
            film.directors.add(person)

        valid_person = [person for person in data.get('persons') if
                        (person.get('enProfession') == 'actor' and
                         person.get('name') is not None and
                         person.get('id') is not None)]
        for p in valid_person:
            person, _ = Actor._actor_manager.update_or_create(name=p.get('name'),
                                                              kp_id=p.get('id'),
                                                              photo=p.get('photo'))
            film.actors.add(person)

        valid_person = [person for person in data.get('persons') if
                        (person.get('enProfession') == 'writer' and
                         person.get('name') is not None and
                         person.get('id') is not None)]
        for p in valid_person:
            person, _ = Writer._writer_manager.update_or_create(name=p.get('name'),
                                                                kp_id=p.get('id'),
                                                                photo=p.get('photo'))
            film.writers.add(person)
    serializer = serializers.FilmSerializer(film)
    return Response(serializer.data)

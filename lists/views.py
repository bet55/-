import asyncio

import requests
from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
import json

from rest_framework.views import APIView

from classes import KP_Movie
from lists import serializers, utils
from lists.models import Film, Director, Genre, Actor, Writer
from utils import convert_movie_info, convert_file, get_api_token
from lists.serializers import FilmSerializer, GenreSerializer
from utils import convert_file
from lists.models import Film
from utils.request_kp_movie import get_movie


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


class AddFilm(APIView):
    def get(self, request):
        return render(request, 'lists/add_movie.html')

    def post(self, request):
        kp_id = request.POST.get('url').split('/')[4]
        kp_data = asyncio.run(get_movie(kp_id))
        if kp_data.get('id') is None or kp_data.get('name') is None:
            return Response(kp_data, status=status.HTTP_400_BAD_REQUEST)

        correct_data = utils.refactor_kp_data(kp_data)
        new_film = utils.save_new_film(correct_data)

        if new_film is None:
            return Response('couldnt save new film (unluck)')

        return Response({'id': new_film.kp_id, 'name': new_film.name}, status=status.HTTP_200_OK)


@api_view()
def response_check(request):
    return Response(data={'message': 'alive'})


@api_view()
def view_postcard(request):
    return render(request, 'lists/postcard.html')


@api_view(['GET'])
def view_movies(request):
    response_format = request.query_params.get('format')
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

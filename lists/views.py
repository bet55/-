import asyncio

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.views import APIView

from classes import KP_Movie, Movie, Note
from lists.models import Film, Director, Genre, Actor, Writer, FilmGenreRelations, Sticker, AppUser
from lists.serializers import FilmSerializer, FilmSmallSerializer, GenreSerializer, UserSerializer, StickerSerializer
from pydantic_models import RateMovieRequestModel
from utils import get_movie, refactor_kp_data, save_new_film


# Create your views here.
class ToWatchList(APIView):
    def get(self, request):
        queryset = Film.mgr.all().filter(is_archive=False).order_by('-rating_kp')
        serializer = FilmSmallSerializer(queryset, many=True)
        return render(request, 'movies.html', context={'data': serializer.data})


class ArchiveList(APIView):
    def get(self, request):
        queryset = Film.mgr.all().filter(is_archive=True).order_by('-rating_kp')
        serializer = FilmSmallSerializer(queryset, many=True)
        return render(request, 'movies.html', context={'data': serializer.data})


class AddFilm(APIView):
    def get(self, request):
        return render(request, 'add_movie.html')

    def post(self, request):
        kp_id = request.POST.get('url').split('/')[4]
        kp_data = asyncio.run(get_movie(kp_id))
        if kp_data.get('id') is None or kp_data.get('name') is None:
            return Response(kp_data, status=status.HTTP_400_BAD_REQUEST)

        correct_data = refactor_kp_data(kp_data)
        new_film = save_new_film(correct_data)

        if new_film is None:
            return Response('couldn`t save new film (unluck)')

        return Response({'id': new_film.kp_id, 'name': new_film.name}, status=status.HTTP_200_OK)


class RateFilm(APIView):
    sticker_model = Sticker()

    def post(self, request):
        user = request.data['user']
        film = request.data['film']
        text = request.data['text']
        rating = request.data['rating']

        self.sticker_model.mgr.create(user=user, film=film, text=text, rating=rating)

    def remove(self, request):
        user = request.data['user']
        film = request.data['film']

        sticker = self.sticker_model.mgr.get(user=user, film=film)
        sticker.delete()


@api_view(['GET'])
def view_movies(request):
    response_format = request.query_params.get('format')
    is_archive = 'archive' in request.path

    mv = Movie()

    if response_format == 'json':
        movies = mv.get_all_movies(is_archive=is_archive)
        return Response(movies)

    users = AppUser.objects.all()
    us_sr = UserSerializer(users, many=True)

    movies = mv.get_all_movies(all_info=False, is_archive=is_archive)

    return render(request, 'movies.html',
                  context={'movies': movies, 'users': us_sr.data, 'is_archive': is_archive})


@api_view(['GET'])
def view_movie_by_id(request, kp_id):
    mv = Movie()
    movie = mv.get_movie(kp_id=kp_id)

    return Response(movie)


# todo error handler view
@api_view(['GET', 'POST'])
def add_movie(request):
    if request.method == 'GET':
        return render(request, 'add_movie.html')

    kp_id = ''.join(char for char in list(request.data.get('kp_id', '')) if char.isdigit())

    mv = Movie()
    movie_id, success = mv.download(kp_id)

    return Response(data={'success': success, 'error': '', 'id': movie_id})


@api_view(['PATCH'])
def change_archive_status(request):
    kp_id = request.data['kp_id']
    is_archive = request.data['is_archive']

    movie = Movie()
    movie_is_changed = movie.change_movie_status(kp_id, is_archive)

    return Response(data={'success': str(movie_is_changed), 'error': '', 'id': kp_id})


@api_view(['DELETE'])
def remove_movie(request):
    kp_id = request.data.get('kp_id')

    if not kp_id:
        return Response(data={'success': False, 'error': 'Lost kp_id', 'id': False})

    movie = Movie()
    movie_is_deleted = movie.remove_movie(kp_id)

    return Response(data={'success': str(movie_is_deleted), 'error': '', 'id': kp_id})


@api_view(['POST', 'PUT'])
def rate_movie(request):
    note_created = Note.create_note(request.data)

    return Response(data={'success': note_created, 'error': ''})


@api_view(['DELETE'])
def remove_rate(request):
    user = request.dat['user']
    film = request.data['film']

    res = Note.remove_note(user, film)

    return Response(data={'success': bool(res), 'error': str(res)})

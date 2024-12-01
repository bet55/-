from rest_framework.decorators import api_view
from adrf.decorators import api_view as asapi_view
from rest_framework.response import Response
from classes import Movie, Note, Tools
from lists.models import AppUser
import json
import asyncio
from django.shortcuts import render
from tools.serializers import UserSerializer


@api_view(['GET'])
def old_format(request):
    response_format = request.query_params.get('format')
    is_archive = 'archive' in request.path

    mv = Movie()

    if response_format == 'json':
        movies = mv.get_all_movies(is_archive=is_archive)
        return Response(movies)

    movies = mv.get_all_movies(all_info=False, is_archive=is_archive)

    return render(request, 'movies_old.html',
                  context={'movies': movies, 'is_archive': is_archive})


@api_view(['GET'])
def view_notes(request):
    notes = Note.get_all_notes()
    return Response(notes)


@api_view(['GET'])
def view_users(request):
    users = AppUser.objects.all()
    ser = UserSerializer(users, many=True)
    return Response(ser.data)


@asapi_view(['GET'])
async def init_project(request):
    tools = Tools()
    res = tools.init_project()
    return Response(res)



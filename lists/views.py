from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from utils.get_api_token import get_api_token


# Create your views here.
@api_view()
def response_check(request):
    return Response(data={'message': 'alive'})


@api_view(['GET'])
def view_movies(request):
    return render(request, 'movie_verse/index.html')


@api_view(['GET'])
def view_archive_movies(request):
    return render(request, 'movie_verse/index.html')


@api_view(['GET', 'POST'])
def add_movie(request):
    return Response({'token': get_api_token()})
    # return render(request, 'movie_verse/index.html')


@api_view(['GET'])
def movies_dump(request):
    with open('utils/movies_dump.json', 'r') as f:
        movies = json.load(f)
    return Response(movies)

from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


# Create your views here.
@api_view()
def response_check(request):
    return Response(data={'message': 'alive'})


@api_view()
def main_page(request):
    return render(request, 'movie_verse/index.html')


@api_view()
def adding_movie(request):
    return render(request, 'movie_verse/index.html')


@api_view()
def movies_list(request):
    with open('templates/movie_verse/db.json', 'r') as f:
        movies = json.load(f)
    return Response(movies)


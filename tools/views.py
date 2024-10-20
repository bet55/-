from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils import convert_file
import json


@api_view()
def response_check(request):
    return Response(data={'message': 'alive'})


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



from rest_framework.decorators import api_view
from adrf.decorators import api_view as asapi_view
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from classes import Movie, Note
from lists.models import AppUser
import json
import asyncio

from tools.serializers import UserSerializer


@api_view(['GET'])
def view_notes(request):
    # st = Sticker.mgr.all()
    # sr = StickerSerializer(st, many=True)
    # return Response(sr.data)

    notes = Note.get_all_notes()
    return Response(notes)


@api_view(['GET'])
def view_users(request):
    users = AppUser.objects.all()
    ser = UserSerializer(users, many=True)
    return Response(ser.data)


@api_view(['GET'])
def create_user(request):
    url = 'http://localhost:8000/static/img/avatars/'
    users = [
        {'username': 'drbloody1', 'first_name': 'Алексей', 'last_name': 'Губин', 'avatar': url + 'drbloody1.jpg'},
        {'username': 'daenillando', 'first_name': 'Александр', 'last_name': 'Бусыгин', 'avatar': url + 'Deputant.png'},
        {'username': 'Deputant', 'first_name': 'Никита', 'last_name': 'Шулаев', 'avatar': url + 'Deputant.jpg'},
        {'username': 'lightthouse', 'first_name': 'Степан', 'last_name': 'Казанцев', 'avatar': url + 'lightthouse1.jpg'},
    ]

    results = []
    for user in users:
        user_model, status = AppUser.objects.update_or_create(**user)
        results.append({user['username']: status})

    return Response(results)


@asapi_view(['GET'])
async def save_movies_to_db(request):
    movies_json = 'data/movies_to_watch_dump.json'
    archive_movies_json = 'data/archive_movies_dump.json'

    failed_movies_file = 'data/failed_movies.json'
    error_file = 'data/save_error.json'

    with open(archive_movies_json, 'r') as f:
        archive_movies = json.load(f)
        archive_movies = [{**arch, **{'is_archive': True}} for arch in archive_movies]

    with open(movies_json, 'r') as f:
        movies = json.load(f)

    all_movies = movies + archive_movies

    async def download(mv_info):
        mv = Movie()
        try:
            await mv.a_download(mv_info.get('id', -1), mv_info)
            return {'success': True, 'id': mv_info.get('id', -1)}
        except Exception as exp:
            return {'success': False, 'id': mv_info.get('id', -1), 'message': str(exp)}

    tasks = [download(movie) for movie in all_movies]
    tasks_result = await asyncio.gather(*tasks)

    success_results_count = len([r for r in tasks_result if r['success'] is True])
    bad_results = [r for r in tasks_result if r['success'] is False]

    with open(failed_movies_file, 'w') as f:
        f.write(json.dumps(bad_results, indent=4, ensure_ascii=False))

    return Response({'success_count': success_results_count, 'all_count': len(all_movies)})


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

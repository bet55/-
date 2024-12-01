import dataclasses
from rest_framework.decorators import api_view
from adrf.decorators import api_view as asapi_view
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from classes import Movie, Note
from lists.models import AppUser
import json
import asyncio
from django.shortcuts import render
from tools.serializers import UserSerializer
import os
import random


class Tools:

    @classmethod
    def get_random_images(cls):
        return {'card': cls.random_card_image(), 'nav': cls.random_nav_image()}

    @classmethod
    def random_card_image(self):
        DEFAULT_IMG = '/static/img/madness/mad16.png'

        folder_path = 'static/img/card_bg'
        file_names = os.listdir(folder_path)
        random_img = random.choice(file_names)

        return f'/static/img/card_bg/{random_img}' if random_img else DEFAULT_IMG

    @classmethod
    def random_nav_image(self):

        DEFAULT_IMG = '/static/retro_images/bird.png'

        folder_path = 'static/img/madness'
        file_names = os.listdir(folder_path)
        random_img = random.choice(file_names)

        return f'/static/img/madness/{random_img}' if random_img else DEFAULT_IMG

    async def init_project(self):
        await self.check_project_pre_creation()
        await self.create_users()
        await self.save_movies_to_db()

    async def check_project_pre_creation(self):
        users = AppUser.objects.all()
        if len(users) > 1:
            raise Exception('В системе уже есть пользователи')
        if len(users) < 1:
            raise Exception('Сперва создайте супер пользователя')

    async def create_users(self):
        url = 'http://localhost:8000/static/img/avatars/'
        users = [
            {'username': 'drbloody1', 'first_name': 'Алексей', 'last_name': 'Губин', 'avatar': url + 'drbloody1.jpg'},
            {'username': 'daenillando', 'first_name': 'Александр', 'last_name': 'Бусыгин', 'avatar': url + 'Deputant.png'},
            {'username': 'Deputant', 'first_name': 'Никита', 'last_name': 'Шулаев', 'avatar': url + 'Deputant.jpg'},
            {'username': 'lightthouse', 'first_name': 'Степан', 'last_name': 'Казанцев', 'avatar': url + 'lightthouse1.jpg'},
        ]

        results = []
        for user in users:
            user_model, status = await AppUser.objects.aupdate_or_create(**user)
            results.append({user['username']: status})

        return results

    async def save_movies_to_db(self) -> dict:
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

        async def export(mv_info):
            mv = Movie()
            try:
                await mv.a_download(mv_info.get('id', -1), mv_info)
                return {'success': True, 'id': mv_info.get('id', -1)}
            except Exception as exp:
                return {'success': False, 'id': mv_info.get('id', -1), 'message': str(exp)}

        tasks = [export(movie) for movie in all_movies]
        tasks_result = await asyncio.gather(*tasks)

        success_results_count = len([r for r in tasks_result if r['success'] is True])
        bad_results = [r for r in tasks_result if r['success'] is False]

        with open(failed_movies_file, 'w') as f:
            f.write(json.dumps(bad_results, indent=4, ensure_ascii=False))

        return {'success_count': success_results_count, 'all_count': len(all_movies)}

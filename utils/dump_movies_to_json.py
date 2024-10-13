import json
from icecream import ic
import pendulum

# Конвертим представление фильма из КП в кастомное, чтобы использовать готовый шаблон наполнения страницы

with open('api_response.json', 'r') as f:
    movie_kp_info = json.load(f)

director = [p['name'] for p in movie_kp_info.get('persons', []) if p.get('enProfession') == 'director'] or 'ඞඞඞ'
released_date = pendulum.parse(movie_kp_info['createdAt']).format('DD/MM/YYYY')
movie_info = {
    "id": movie_kp_info.get('id', 'ඞඞඞ'),
    "title": movie_kp_info.get('name', 'ඞඞඞ'),
    "director": director[0],
    "watched": False,
    "liked": False,
    "on_watchlist": True,
    "poster": movie_kp_info.get('poster', {}).get('url', 'ඞඞඞ'),
    "runtime": movie_kp_info.get('movieLength', 'ඞඞඞ'),
    "released_date": released_date,
    "description": movie_kp_info.get('description', 'ඞඞඞ'),
}
with open('movies_dump.json', 'w') as f:
    f.write(json.dumps([movie_info] * 20, indent=4, ensure_ascii=False))

ic(movie_info)

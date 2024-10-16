import json
from icecream import ic
import pendulum


# Конвертим представление фильма из КП в кастомное, чтобы использовать готовый шаблон наполнения страницы


def convert_movie_info(movie_kp_info: dict) -> dict:
    director = [p['name'] for p in movie_kp_info.get('persons', []) if p.get('enProfession') == 'director'] or 'ඞඞඞ'
    released_date = pendulum.parse(movie_kp_info.get('createdAt', pendulum.now().to_date_string())).format('DD/MM/YYYY')
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
    return movie_info


def convert_file(movies: list, file_name: str) -> int:
    converted_info = []
    movies_count = 0
    for movie in movies:
        converted_info.append(convert_movie_info(movie))
        movies_count += 1

    with open(file_name, 'w') as f:
        f.write(json.dumps(converted_info, indent=4, ensure_ascii=False))

    return movies_count



if __name__ == 'main':
    with open('../data/movies_to_watch_dump.json', 'r') as f:
        movies = json.load(f)

    with open('../data/archive_movies_dump.json', 'r') as f:
        archive_movies = json.load(f)

    mc = convert_file(movies, '../data/movies_to_watch_old.json')
    amc = convert_file(archive_movies, '../data/archive_movies_old.json')
    ic(mc, amc)

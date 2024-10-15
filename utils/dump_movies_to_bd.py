import json
from lists.models import Film, Actor, Director, Writer, Genre
from icecream import ic


def get_param():
    pass


def get_persons(person_list: list, person_name: str):
    filtered_persons = []
    for person in person_list:
        if person['enProfession'] != person_name:
            continue
        person_info = {
            'kp_id': person['id'],
            'name': person['name'],
            'photo': person['photo'],
        }
        filtered_persons.append(person_info)

    return filtered_persons


def convert_movie_info(movie_info: dict):
    kp_id = movie_info['id']
    name = movie_info['name']
    countries = movie_info['countries'].values()
    genres = movie_info['genres'].values()
    directors = get_persons(movie_info['persons'], 'director')
    actors = get_persons(movie_info['persons'], 'actor')
    writers = get_persons(movie_info['persons'], 'writer')
    budget = movie_info['budget']['value']
    fees = movie_info['fees']['value']
    premiere = movie_info['premiere']['world']
    description = movie_info['description']
    short_description = movie_info['shortDescription']
    slogan = movie_info['slogan']
    duration = movie_info['movieLength']
    poster = movie_info['poster']['url']
    rating_kp = movie_info['rating']['kp']
    rating_imdb = movie_info['rating']['imdb']
    votes_kp = movie_info['votes']['kp']
    votes_imdb = movie_info['votes']['imdb']


def convert_file(file_path: str):
    with open(file_path, 'r') as f:
        movies_dump = json.load(f)

    movies_count = 0
    broken_movies_ids = []
    for movie in movies_dump:
        try:
            convert_movie_info(movie)
            movies_count += 1
        except Exception:
            broken_movies_ids.append(movie['id'])

    return movies_count


movies_dump_file = '../data/movies_to_watch_dump.json'
archive_movies_dump_file = '../data/archive_movies_dump.json'

ic(convert_file(movies_dump_file))
ic(convert_file(archive_movies_dump_file))

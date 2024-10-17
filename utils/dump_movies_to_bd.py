import json
from lists.models import Film, Actor, Director, Writer, Genre
from icecream import ic


def get_persons(person_list: list, person_name: str):
    filtered_persons = []
    for person in person_list:
        if person['enProfession'] != person_name:
            continue

        pid = person.get('id')
        pname = person.get('name')
        pphoto = person.get('photo')

        required_data = [bool(pid), bool(pname)]
        if not all(required_data):
            continue

        person_info = {
            'kp_id': pid,
            'name': pname,
            'photo': pphoto,
        }
        filtered_persons.append(person_info)

    return filtered_persons


def convert_movie_info(movie_info: dict, is_archive: bool = False):
    # mock for none values
    n_name = 'БЕЗЫМЯННЫЙ'
    n_url = 'https://banner2.cleanpng.com/20180715/yag/aavjmwzok.webp'
    n_slogan = '...'
    n_description = '...'
    n_short_description = '...'
    n_date = '01.01.1970'

    required_data = [movie_info.get('id'), movie_info.get('name')]
    if not all(required_data):
        return 'Отсутсвуют необходимые данные о фильме'

    kp_id = movie_info.get('id', -1)
    name = movie_info.get('name', n_name)
    countries = [c['name'] for c in movie_info['countries'] if c.get('name')]
    genres = [c['name'] for c in movie_info['genres'] if c.get('name')]
    directors = get_persons(movie_info['persons'], 'director')
    actors = get_persons(movie_info['persons'], 'actor')
    writers = get_persons(movie_info['persons'], 'writer')
    budget = movie_info.get('budget', {}).get('value', -1)
    fees = movie_info.get('fees', {}).get('world', {}).get('value', -1)
    premiere = movie_info.get('premiere', {}).get('world', n_date)
    description = movie_info.get('description', n_description)
    short_description = movie_info.get('shortDescription', n_short_description)
    slogan = movie_info.get('slogan', n_slogan)
    duration = 0 if not movie_info.get('movieLength', 0) else movie_info['movieLength']
    poster = movie_info.get('poster', {}).get('url', n_url)
    rating_kp = movie_info.get('rating', {}).get('kp', 0.0)
    rating_imdb = movie_info.get('rating', {}).get('imdb', 0.0)
    votes_kp = movie_info.get('votes', {}).get('kp', 0)
    votes_imdb = movie_info.get('votes', {}).get('imdb', 0)

    # return movie_info.get('id', -1)
    m_film = Film(
        kp_id=kp_id,
        name=name,
        countries=countries,
        budget=budget,
        fees=fees,
        premiere=premiere,
        description=description,
        short_description=short_description,
        slogan=slogan,
        duration=duration,
        poster=poster,
        rating_kp=rating_kp,
        rating_imdb=rating_imdb,
        votes_kp=votes_kp,
        votes_imdb=votes_imdb,
        is_archive=is_archive
    )

    m_film.save()

    for genre in genres:
        m_genre, _ = Genre._genre_manager.update_or_create(name=genre)
        m_film.genres.add(m_genre)

    for actor in actors:
        m_actor, _ = Actor._actor_manager.update_or_create(kp_id=actor['kp_id'], name=actor['name'], photo=actor['photo'])
        m_film.actors.add(m_actor)

    for writer in writers:
        m_writer, _ = Writer._writer_manager.update_or_create(kp_id=writer['kp_id'], name=writer['name'], photo=writer['photo'])
        m_film.writers.add(m_writer)

    for director in directors:
        m_director, _ = Director._director_manager.update_or_create(kp_id=director['kp_id'], name=director['name'], photo=director['photo'])
        m_film.directors.add(m_director)

    return movie_info['id']


def check_errors():
    with open('../data/save_error.json', 'r') as f:
        errs = json.load(f)

    pers = []
    for er in errs:
        try:
            # ic(er['id'], er['name'])
            if er['id'] == 3011:
                pers = er['persons']
        except Exception as exp:
            ic(er['id'], exp)

    for per in pers:
        ic(per['name'])


def convert_file(file_path: str, error_movies_path: str, error_path: str, is_archive: bool):
    with open(file_path, 'r') as f:
        movies_dump = json.load(f)

    movies_count = 0
    broken_movies_ids = []
    broken_movies = []
    for movie in movies_dump:
        try:
            convert_movie_info(movie, is_archive)
            movies_count += 1
        except Exception as e:
            broken_movies_ids.append({'id': movie.get('id', -1), 'exp': str(e)})
            broken_movies.append(movie)

    with open(error_movies_path, 'w') as f:
        f.write(json.dumps(broken_movies_ids, indent=4, ensure_ascii=False))

    with open(error_path, 'w') as f:
        f.write(json.dumps(broken_movies, indent=4, ensure_ascii=False))

    return movies_count


if __name__ == 'main':
    movies_dump_file = 'data/movies_to_watch_dump.json'
    archive_movies_dump_file = 'data/archive_movies_dump.json'
    #
    # ic(convert_file(movies_dump_file, 'movies_error.json'))
    # ic(convert_file(archive_movies_dump_file, 'archive_error.json'))




from lists.models import Film, Actor, Director, Writer, Genre

# Обновление метода сериализации данных из api кинопоиска и записи их в бд

def refactor_kp_data(kp_data: dict) -> dict:
    #returns only persons that has correct role, name and id
    def _get_valid_persons(data: dict, role: str) -> list:
        _list_of_persons = []
        for person in [person for person in data if
                       (person.get('enProfession') == role and
                        person.get('name') is not None and
                        person.get('id') is not None)]:
            _list_of_persons.append({'name': person.get('name'),
                                     'kp_id': person.get('id'),
                                     'photo': person.get('photo')})
        return _list_of_persons

    #all data about film that kp provided, unpuck this into new film instance
    #doesnt check if name/id is present, validators and middlewear does this job
    _film_data = {}
    #iterate through these list and make new instances, then unpuck dicts into them
    _related_actors = []
    _related_directors = []
    _related_writers = []
    _related_genres = []

    if kp_data.get('id'):
        _film_data['kp_id'] = kp_data['id']
    if kp_data.get('name'):
        _film_data['name'] = kp_data['name']
    if kp_data.get('countries') and len(kp_data.get('countries')):
        _film_data['countries'] = [country.get('name') for country in kp_data.get('countries')]
    if kp_data.get('budget', {}).get('value'):
        _film_data['budget'] = kp_data.get('budget').get('value', 'unknown')
    if kp_data.get('fees', {}).get('world', {}).get('value'):
        _film_data['fees'] = kp_data.get('fees').get('world').get('value')
    if kp_data.get('premiere', {}).get('world'):
        _film_data['premiere'] = kp_data.get('premiere').get('world')
    if kp_data.get('description'):
        _film_data['description'] = kp_data['description']
    if kp_data.get('short_description'):
        _film_data['short_description'] = kp_data.get('short_description')
    if kp_data.get('slogan'):
        _film_data['slogan'] = kp_data.get('slogan')
    if kp_data.get('duration'):
        _film_data['duration'] = kp_data.get('duration')
    if kp_data.get('poster', {}).get('url'):
        _film_data['poster'] = kp_data.get('poster').get('url')
    if kp_data.get('rating', {}).get('kp'):
        _film_data['rating_kp'] = kp_data.get('rating').get('kp')
    if kp_data.get('rating', {}).get('imdb'):
        _film_data['rating_imdb'] = kp_data.get('rating').get('imdb')
    if kp_data.get('votes', {}).get('kp'):
        _film_data['votes_kp'] = kp_data.get('votes').get('kp')
    if kp_data.get('votes', {}).get('imdb'):
        _film_data['votes_imdb'] = kp_data.get('votes').get('imdb')

    if kp_data.get('genres') and len(kp_data.get('genres')):
        for genre in kp_data.get('genres'):
            _related_genres.append({'name': genre.get('name')})

    _related_actors = _get_valid_persons(kp_data.get('persons'), 'actor')
    _related_directors = _get_valid_persons(kp_data.get('persons'), 'director')
    _related_writers = _get_valid_persons(kp_data.get('persons'), 'writer')

    correct_data = {'film_data': _film_data,
                    'related_actors': _related_actors,
                    'related_directors': _related_directors,
                    'related_writers': _related_writers,
                    'related_genres': _related_genres}
    return correct_data


def save_new_film(data: dict) -> Film:
    film = Film(**data.get('film_data'))
    film.save()

    for actor in data.get('related_actors'):
        actor = Actor(**actor)
        actor.save()
        film.actors.add(actor)

    for director in data.get('related_directors'):
        director = Director(**director)
        director.save()
        film.directors.add(director)

    for writer in data.get('related_writers'):
        writer = Writer(**writer)
        writer.save()
        film.writers.add(writer)

    for genre in data.get('related_genres'):
        genre = Genre(**genre)
        genre.save()
        film.genres.add(genre)

    return film

from classes.kp import KP_Movie
from lists.models import Film as FilmModel, Actor as ActorModel, Writer as WriterModel, Director as DirectorModel, Genre as GenreModel
from lists.serializers import FilmSerializer, FilmSmallSerializer
from pydantic_models import KPFilmModel, KpFilmPersonModel, KpFilmGenresModel
import json
from typing import Any
from icecream import ic
from collections import namedtuple


class Genre:
    pass


class Actor:
    pass


class Writer:
    pass


class Director:
    pass


class StickyNotes:
    pass


class Movie:
    KPEntities = namedtuple('KPEntities', ['movie', 'persons', 'genres'])

    def get_movie(self, kp_id: int | str) -> dict:
        film_model = FilmModel.mgr.filter(kp_id=kp_id)
        serialize = FilmSerializer(film_model)
        return serialize.data

    def get_all_movies(self, all_info: bool = True, is_archive: bool = False) -> dict | list:
        film_model = FilmModel.mgr.filter(is_archive=is_archive).values()

        if all_info:
            serialize = FilmSerializer(film_model, many=True)
            films = {film['kp_id']: film for film in serialize.data}
        else:
            serialize = FilmSmallSerializer(film_model, many=True)
            films = serialize.data
        return films

    def change_movie_status(self, kp_id: int | str, is_archive: bool):
        film_model = FilmModel.mgr.get(kp_id=kp_id)
        film_model.is_archive = is_archive
        return film_model.save()

    def remove_movie(self, kp_id: int | str):
        film_model = FilmModel.mgr.get(kp_id=kp_id)
        return film_model.delete()

    def download(self, kp_id: int | str) -> tuple[int, bool]:

        kp_client = KP_Movie()
        api_response = kp_client.get_movie_by_id(kp_id)

        converted_response = self._response_preprocess(api_response)

        save_movies = self._save_movie_to_db(converted_response)

        return api_response.get('id', -1), save_movies[1]

    def _save_movie_to_db(self, movie_info: KPEntities):
        movie, persons, genres = movie_info

        movie_model, m_status = FilmModel.mgr.update_or_create(**movie)

        a, d, w, g = self._create_models_counstuctor_list(persons, genres)
        ActorModel.mgr.bulk_create(a, update_conflicts=True, update_fields=['photo'], unique_fields=['kp_id'])
        DirectorModel.mgr.bulk_create(d, update_conflicts=True, update_fields=['photo'], unique_fields=['kp_id'])
        WriterModel.mgr.bulk_create(w, update_conflicts=True, update_fields=['photo'], unique_fields=['kp_id'])
        GenreModel.mgr.bulk_create(g, update_conflicts=True, update_fields=['watch_counter'], unique_fields=['name'])

        movie_model.actors.set(a)
        movie_model.directors.set(d)
        movie_model.writers.set(w)
        movie_model.genres.set(g)

        return movie_model, m_status

    async def a_download(self, kp_id: int | str, kp_scheme: dict = None) -> tuple[int, bool]:

        if not kp_scheme:
            kp_client = KP_Movie()
            api_response = kp_client.get_movie_by_id(kp_id)
        else:
            api_response = kp_scheme

        converted_response = self._response_preprocess(api_response)

        save_movies = await self._a_save_movie_to_db(converted_response)

        return api_response.get('id', -1), save_movies[1]

    async def _a_save_movie_to_db(self, movie_info: KPEntities):
        movie, persons, genres = movie_info
        movie_model, m_status = await FilmModel.mgr.aupdate_or_create(**movie)

        a, d, w, g = self._create_models_counstuctor_list(persons, genres)

        await ActorModel.mgr.abulk_create(a, update_conflicts=True, update_fields=['photo'], unique_fields=['kp_id'])
        await DirectorModel.mgr.abulk_create(d, update_conflicts=True, update_fields=['photo'], unique_fields=['kp_id'])
        await WriterModel.mgr.abulk_create(w, update_conflicts=True, update_fields=['photo'], unique_fields=['kp_id'])
        await GenreModel.mgr.abulk_create(g, update_conflicts=True, update_fields=['watch_counter'], unique_fields=['name'])

        await movie_model.actors.aset(a)
        await movie_model.directors.aset(d)
        await movie_model.writers.aset(w)
        await movie_model.genres.aset(g)

        return movie_model, m_status

    def _create_models_counstuctor_list(self, persons: dict[str, list], genres: list) -> tuple[list, list, list, list]:
        actors = [ActorModel(**pers) for pers in persons['actor']]
        directors = [DirectorModel(**pers) for pers in persons['director']]
        writers = [WriterModel(**pers) for pers in persons['writer']]
        genres = [GenreModel(**gen) for gen in genres]

        return actors, directors, writers, genres

    def _response_preprocess(self, movie_info: dict) -> KPEntities:

        movie = self._movie_preprocess(movie_info)
        persons = self._persons_preprocess(movie_info)
        genres = self._genres_preprocess(movie_info)

        return self.KPEntities(movie, persons, genres)

    def _genres_preprocess(self, movie_info: dict) -> list[str]:
        modeling = KpFilmGenresModel(genres=movie_info.get('genres'))
        formated_genres = modeling.dict().get('genres')
        return formated_genres

    def _movie_preprocess(self, movie_info: dict) -> dict[str, int | str]:
        modeling = KPFilmModel(**movie_info)
        formated_movie = modeling.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True)
        return formated_movie

    def _persons_preprocess(self, movie_info: dict) -> dict[str, list]:
        persons = {'actor': [], 'writer': [], 'director': []}

        for p in movie_info.get('persons', []):
            if not all([p.get('id'), p.get('name')]):
                continue

            try:
                persons[p['enProfession']].append(KpFilmPersonModel(**p).model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True))
            except KeyError:
                continue

        return persons

from classes.kp import KP_Movie
from lists.models import Film as FilmModel, Actor as ActorModel, Writer as WriterModel, Director as DirectorModel, Genre as GenreModel
from lists.serializers import FilmSerializer, FilmSmallSerializer
from pydantic_models import KPFilmModel, KpFilmPersonModel, KpFilmGenresModel
import json
from typing import Any
from icecream import ic


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
    def get_movie(self, kp_id: int | str) -> dict:
        film_model = FilmModel._film_manager.filter(kp_id=kp_id)
        serialize = FilmSerializer(film_model)
        return serialize.data

    def get_all_movies(self, all_info: bool = True, is_archive: bool = False) -> dict | list:
        film_model = FilmModel._film_manager.filter(is_archive=is_archive).values()

        if all_info:
            serialize = FilmSerializer(film_model, many=True)
            films = {film['kp_id']: film for film in serialize.data}
        else:
            serialize = FilmSmallSerializer(film_model, many=True)
            films = serialize.data
        return films

    def change_movie_status(self, kp_id: int | str):
        ...

    def remove_movie(self, kp_id: int | str):
        pass

    def download(self, kp_id: int | str) -> tuple[int, bool]:
        # TODO bulk_create

        kp_client = KP_Movie()
        api_response = kp_client.get_movie_by_id(kp_id)

        movie = self._movie_preprocess(api_response)
        persons = self._persons_preprocess(api_response)
        genres = self._genres_preprocess(api_response)

        save_movies = self._save_movie_to_db(movie, persons, genres)

        return api_response.get('id', -1), save_movies[1]

    def _save_movie_to_db(self, movie_info: dict, persons: dict, genres: list):
        # persons_models = {'actor': Actor, 'writer': Writer, 'director': Director}

        movie_model, m_status = FilmModel._film_manager.update_or_create(**movie_info)

        for genre in genres:
            genre_model, _status = GenreModel._genre_manager.update_or_create(**genre)
            movie_model.genres.add(genre_model)

        for actor in persons['actor']:
            actor_model, _status = ActorModel._actor_manager.update_or_create(**actor)
            movie_model.actors.add(actor_model)

        for writer in persons['writer']:
            writer_model, _status = WriterModel._writer_manager.update_or_create(**writer)
            movie_model.writers.add(writer_model)

        for director in persons['director']:
            director_model, _status = DirectorModel._director_manager.update_or_create(**director)
            movie_model.directors.add(director_model)

        return movie_model, m_status

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

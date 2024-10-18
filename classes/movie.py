from classes.kp import KP_Movie
from lists.models import Film, Actor, Writer, Director, Genre
from pydantic_models import KPFilmModel, KpFilmPersonModel, KpFilmGenresModel
import json
from typing import Any
from icecream import ic


class Movie:
    def get_movie(self, kp_id: int | str):
        pass

    def get_all_movies(self, is_archive: bool = False):
        pass

    def change_movie_status(self, kp_id: int | str):
        pass

    def remove_movie(self, kp_id: int | str):
        pass

    def download(self, kp_id: int | str) -> tuple[int, bool]:
        # TODO обработать ошибки
        # TODO проверить работу с жанрами
        # TODO отсечь модели без данных

        kp_client = KP_Movie()
        api_response = kp_client.get_movie_by_id(kp_id)

        movie = self._movie_preprocess(api_response)
        persons = self._persons_preprocess(api_response)
        genres = self._genres_preprocess(api_response)

        save_movies = self._save_movie_to_db(movie, persons, genres)

        return api_response['kp_id'], save_movies

    def _save_movie_to_db(self, movie_info: dict, persons: dict, genres: list):
        # persons_models = {'actor': Actor, 'writer': Writer, 'director': Director}

        movie_model = Film(**movie_info)
        movie_model.save()

        for genre in genres:
            genre_model, _status = Genre._genre_manager.update_or_create(**genre)
            movie_model.genres.add(genre_model)

        for actor in persons['actor']:
            actor_model, _status = Actor._actor_manager.update_or_create(**actor)
            movie_model.actors.add(actor_model)

        for writer in persons['writer']:
            writer_model, _status = Writer._writer_manager.update_or_create(**writer)
            movie_model.writers.add(writer_model)

        for director in persons['director']:
            director_model, _status = Director._director_manager.update_or_create(**director)
            movie_model.directors.add(director_model)

        return True

    def _genres_preprocess(self, movie_info: dict) -> list[str]:
        formated_genres = []
        for genre in movie_info.get('genres', []):
            modeling = KpFilmGenresModel(**genre)
            formated_genres.append(modeling.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True))

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

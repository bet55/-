from django.urls import path

from lists.views import (response_check, view_movies, add_movie, save_movies_to_db, ToWatchList, ArchiveList,
                         view_movie_by_id, view_postcard, view_movies_old_format, AddFilm)

urlpatterns = [
    path('', view_postcard),

    path('movies', view_movies),
    path('movies/<int:kp_id>', view_movie_by_id),
    path('movies/archive', view_movies),
    path('movies/add', add_movie),

    # statistc
    # features / games

    path('tools/check', response_check),
    path('tools/old_format', view_movies_old_format),
    path('tools/save_to_db', save_movies_to_db),

    path('to_watch_list', ToWatchList.as_view()),
    path('archive_list', ArchiveList.as_view()),
    path('add_film', AddFilm.as_view()),
]

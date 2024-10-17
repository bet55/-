from django.urls import path

from lists.views import (response_check, view_movies, add_movie, save_movies_to_db, ToWatchList, ArchiveList,
                         view_movie_by_id, view_postcard, view_movies_old_format, do_shit)

urlpatterns = [
    path('', view_postcard),

    path('movies', view_movies),
    path('movies/<int:kp_id>', view_movie_by_id),
    path('movies/archive', view_movies),
    path('movies/add', add_movie),

    path('tools/check', response_check),
    path('tools/old_format', view_movies_old_format),
    path('tools/save_to_db', save_movies_to_db),
    path('tools/do_shit', do_shit),

    path('to_watch_list', ToWatchList.as_view()),
    path('archive_list', ArchiveList.as_view()),
]

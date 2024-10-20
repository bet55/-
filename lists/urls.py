from django.urls import path

from lists.views import view_movies, add_movie, ToWatchList, ArchiveList, view_movie_by_id, view_postcard, AddFilm

urlpatterns = [
    path('', view_postcard),

    path('movies', view_movies),
    path('movies/<int:kp_id>', view_movie_by_id),
    path('movies/archive', view_movies),
    path('movies/add', add_movie),

    # statistc
    # features / games


    path('to_watch_list', ToWatchList.as_view()),
    path('archive_list', ArchiveList.as_view()),
    path('add_film', AddFilm.as_view()),
]

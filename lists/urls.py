from django.urls import path

from lists.views import view_movies, add_movie, ToWatchList, ArchiveList, view_movie_by_id, AddFilm, remove_movie, \
    change_archive_status, rate_movie

urlpatterns = [

    path('', view_movies),
    path('archive', view_movies),
    path('<int:kp_id>', view_movie_by_id),

    path('add', add_movie),
    path('remove', remove_movie),
    path('change_archive', change_archive_status),

    path('rate', rate_movie),

]

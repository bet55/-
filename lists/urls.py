from django.urls import path

from lists.views import view_movies, add_movie, ToWatchList, ArchiveList, view_movie_by_id, AddFilm, remove_movie, change_archive_status

urlpatterns = [

    path('', view_movies),
    path('<int:kp_id>', view_movie_by_id),
    path('archive', view_movies),
    path('add', add_movie),
    path('remove', remove_movie),
    path('change_archive', change_archive_status),

    # statistc
    # features / games


    # path('to_watch_list', ToWatchList.as_view()),
    # path('archive_list', ArchiveList.as_view()),
    # path('add_film', AddFilm.as_view()),
]

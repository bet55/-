from django.urls import path

from lists.views import response_check, view_movies, view_archive_movies, add_movie, movies_dump, save_movies_to_db

urlpatterns = [
    path('check', response_check),
    path('', view_movies),
    path('archive', view_archive_movies),
    path('add', add_movie),
    path('list', movies_dump),
    path('save_to_db', save_movies_to_db)
]

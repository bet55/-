from django.urls import path

from lists.views import response_check, view_movies, add_movie, view_movies_old_format, save_movies_to_db, view_movie_by_id, view_postcard

urlpatterns = [
    path('', view_postcard),

    path('movies', view_movies),
    path('movies/<int:kp_id>', view_movie_by_id),
    path('movies/archive', view_movies),
    path('movies/add', add_movie),

    path('tools/check', response_check),
    path('tools/old_format', view_movies_old_format),
    path('tools/save_to_db', save_movies_to_db)
]

from django.urls import path

from tools.views import response_check, save_movies_to_db, view_movies_old_format, create_user, view_users, view_notes, layout

urlpatterns = [
    path('check', response_check),
    path('old_format', view_movies_old_format),
    path('save_to_db', save_movies_to_db),
    path('create_users', create_user),
    path('users', view_users),
    path('notes', view_notes),
    path('based', layout),

]

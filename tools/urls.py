from django.urls import path

from tools.views import view_users, view_notes, init_project, import_films, create_users

urlpatterns = [
    path('init_project', init_project),

    path('create_users', create_users),
    path('import_films', import_films),

    path('users', view_users),
    path('notes', view_notes),

]

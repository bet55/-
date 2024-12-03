from django.urls import path

from tools.views import view_users, view_notes, init_project

urlpatterns = [
    path('init_project', init_project),
    path('users', view_users),
    path('notes', view_notes),

]

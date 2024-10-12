from django.urls import path

from lists.views import response_check, main_page, adding_movie, movies_list

urlpatterns = [
    path('check', response_check),
    path('', main_page),
    path('add', adding_movie),
    path('list', movies_list),
]

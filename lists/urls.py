from django.urls import path

from lists.views import hello_world

urlpatterns = [
    path('', hello_world),
]

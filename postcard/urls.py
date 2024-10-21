from django.urls import path

from postcard.views import view_postcard

urlpatterns = [
    path('', view_postcard),

]

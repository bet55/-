from django.urls import path

from features.views import carousel

urlpatterns = [

    path('carousel', carousel),


]

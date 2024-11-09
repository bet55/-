from django.urls import path

from statistic.views import overall_stats, movies_stats

urlpatterns = [
    path('', movies_stats)

]

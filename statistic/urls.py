from django.urls import path

from statistic.views import overall_stats, movies_stats

urlpatterns = [
    path('', overall_stats),
    path('test', movies_stats)

]

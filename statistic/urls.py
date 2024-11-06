from django.urls import path

from statistic.views import overall_stats

urlpatterns = [
    path('', overall_stats),

]

from rest_framework.decorators import api_view
from django.shortcuts import render
from classes import Statistic
from rest_framework.response import Response


@api_view()
def overall_stats(request):
    return render(request, 'statistc.html')


@api_view(['GET'])
def movies_stats(request):
    s = Statistic()
    res = s.total_watch_hours()
    return Response(res)

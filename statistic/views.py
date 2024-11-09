from rest_framework.decorators import api_view
from django.shortcuts import render
from classes import Statistic
from rest_framework.response import Response


@api_view()
def overall_stats(request):
    return render(request, 'statistic.html')


@api_view(['GET'])
def movies_stats(request):
    stat = Statistic.get_movies_statistic()
    fig = Statistic.draw()
    return render(request, template_name='statistic.html', context={'graph_div': fig, 'statistic': stat})

from rest_framework.decorators import api_view
from django.shortcuts import render
from classes import Statistic, Tools
from rest_framework.response import Response


#  Добавить анимацию пересчета  цифр
# https://codepen.io/r-i-c-h/pen/BaXGZXx

@api_view()
def overall_stats(request):
    return render(request, 'statistic.html')


@api_view(['GET'])
def movies_stats(request):
    stat = Statistic.get_movies_statistic()
    fig = Statistic.draw()
    random_images = Tools.get_random_images()
    return render(request, template_name='statistic.html', context={'graph_div': fig, 'statistic': stat, 'random': random_images})

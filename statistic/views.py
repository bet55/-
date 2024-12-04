from rest_framework.decorators import api_view
from django.shortcuts import render
from classes import Statistic, Tools
from rest_framework.response import Response

from lists.models import AppUser
from lists.serializers import UserSerializer


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
    users = AppUser.objects.all()
    us_sr = UserSerializer(users, many=True)

    return render(request, template_name='statistic.html', context={
        'graph_div': fig,
        'statistic': stat,
        'random': random_images,
        'users': us_sr.data
    })

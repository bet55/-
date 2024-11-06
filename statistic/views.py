from rest_framework.decorators import api_view
from django.shortcuts import render


@api_view()
def overall_stats(request):
    return render(request, 'statistc.html')


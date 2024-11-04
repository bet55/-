from rest_framework.decorators import api_view
from django.shortcuts import render


@api_view()
def view_postcard(request):
    return render(request, 'postcard.html')


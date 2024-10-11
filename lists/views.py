from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view()
def hello_world(request):
    return render(request, 'test.html', context={'hello': 'world'})

from rest_framework.decorators import api_view
from adrf.decorators import api_view as asapi_view
from rest_framework.response import Response
from classes import Movie, Note, Tools
from lists.models import AppUser
import json
import asyncio
from django.shortcuts import render
from tools.serializers import UserSerializer



@api_view(['GET'])
def view_notes(request):
    notes = Note.get_all_notes()
    return Response(notes)


@api_view(['GET'])
def view_users(request):
    users = AppUser.objects.all()
    ser = UserSerializer(users, many=True)
    return Response(ser.data)


@asapi_view(['GET'])
async def init_project(request):
    tools = Tools()
    res = tools.init_project()
    return Response(res)



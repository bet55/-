from adrf.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from postcard.models import Postcard
from postcard.serializers import PostcardSerializer


@api_view()
def view_postcard(request):
    return render(request, 'postcard.html')


class PostCardViewSet(APIView):
    def get(self, request):
        postcard = Postcard.objects.get(pk=request.data['id'])
        serializer = PostcardSerializer(postcard)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostcardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        postcard = Postcard.objects.get(pk=request.data['id'])
        serializer = PostcardSerializer(postcard, data=request.data)
        if serializer.is_valid():
            serializer.update(postcard, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            postcard = Postcard.objects.get(pk=request.data['id'])
            postcard.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Postcard.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

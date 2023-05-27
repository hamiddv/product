from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *


@api_view(['GET'])
def aboutView(requset):
    about = About.objects.all()
    serializer = AboutSerializer(
        about,
        many=True
    )

    return Response(
        serializer.data
    )


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = [
            'title',
            'img',
            'discription',
        ]

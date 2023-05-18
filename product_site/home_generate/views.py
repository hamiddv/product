from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import HomeCustom
from rest_framework import serializers
from rest_framework.response import Response


class Home_serializer(serializers.ModelSerializer):
    class Meta:
        model = HomeCustom
        fields = [
            'id',
            'icon',
            'title',
            'details',
        ]


@api_view(
    [
        "GET",
    ]
)
def HomeProductApi(request):
    products = HomeCustom.objects.all()
    serializer = Home_serializer(
        products,
        many=True
    )
    return Response(
        serializer.data
    )
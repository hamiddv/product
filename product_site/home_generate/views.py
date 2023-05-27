from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
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


class IconSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteIcon
        fields = [
            "icon",
            "hero_image_one",
            "hero_image_two"
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


@api_view(
    [
        "GET",
    ]
)
def home_icon_img(request):
    icon = SiteIcon.objects.all()
    serializer = IconSiteSerializer(
        icon,
        many=True
    ).data


    return Response(
        serializer
    )
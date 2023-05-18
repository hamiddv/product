from django.http import HttpResponse

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from .models import Product
from django.core.files import File
from django.conf import settings
import requests
from io import BytesIO
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
from .models import *


@api_view(['get'])
def HomeProductApi(request):
    products = Product.objects.all()
    serializer = HomeProductSerializer(
        products,
        many=True
    )
    return Response(
        serializer.data
    )


@api_view(['get'])
def IdProductApi(request, id):
    products = Product.objects.get(id=id)
    Product.increase_views(id=id)
    serializer = AllProductSerializer(
        products
    )
    return Response(
        serializer.data
    )


@api_view(['get'])
def AllCategoryApi(request, category):
    products = Product.objects.get(category=category)
    serializer = HomeProductSerializer(
        products,
        many=True
    )
    return Response(
        serializer.data
    )


@api_view(['get'])
def AllCompanyApi(request, company):
    products = Product.objects.get(company=company)
    serializer = HomeProductSerializer(
        products,
        many=True
    )
    return Response(
        serializer.data
    )


@api_view(['get'])
def AllCompanyApi(request, company):
    products = Product.objects.get(company=company)
    serializer = HomeProductSerializer(
        products,
        many=True
    )
    return Response(
        serializer.data
    )


@api_view(['get'])
def MaxPriceiApi(request, price):
    products = Product.objects.filter(price__lt=100)
    print(products)
    serializer = HomeProductSerializer(
        products,
        many=True
    )
    return Response(
        serializer.data
    )


class HomeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image',
        ]


class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image_one'
            'image_two',
            'image_three',
            'image_four',
            'image_five',
            'color_one'
            'color_two',
            'color_three',
            'color_four',
            'color_five',
            'category',
            'company',
            'category',
            'views',
        ]



import random

from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound

from django.shortcuts import render, get_object_or_404
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
def AllProductApi(request):
    try:
        products = Product.objects.all()
        serializer = HomeProductSerializer(
            products,
            many=True
        )
        return Response(
            serializer.data
        )
    except Product.DoesNotExist:
        return HttpResponseNotFound("product not found")
        # return HttpResponseServerError("خطای سرور رخ داد.")


@api_view(['get'])
def HomeProductApi(request):
    last_id = Product.objects.latest('id').id
    first_id = Product.objects.first().id
    print('#' * 20)
    print(first_id)

    product_1 = Product.objects.get(id=(random.randint(first_id, last_id)))
    product_2 = Product.objects.get(id=(random.randint(first_id, last_id)))
    product_3 = Product.objects.get(id=(random.randint(first_id, last_id)))

    serializer1 = HomeProductSerializer(product_1)
    serializer2 = HomeProductSerializer(product_2)
    serializer3 = HomeProductSerializer(product_3)

    data = {
        'Product1': serializer1.data,
        'Product2': serializer2.data,
        'Product3': serializer3.data,
    }

    return Response(data)


@api_view(['get'])
def IdProductApi(request, id):
    try:
        products = Product.objects.get(id=id)
        serializer = AllProductSerializer(
            products
        )
        return Response(
            serializer.data
        )
    except Product.DoesNotExist:
        return HttpResponseNotFound("product not found")


# @api_view(['get'])
# def AllCategoryApi(request, category):
#     try:
#         products = Product.objects.filter(category=category)
#         serializer = HomeProductSerializer(
#             products,
#             many=True
#         )
#         return Response(
#             serializer.data
#         )
#     except Product.DoesNotExist:
#         return HttpResponseNotFound("product not found")
#         # return HttpResponseServerError("this category dose not exist")


# @api_view(['get'])
# def AllCompanyApi(request, company):
#     try:
#         products = Product.objects.filter(company=company)
#         serializer = HomeProductSerializer(
#             products,
#             many=True
#         )
#         return Response(
#             serializer.data
#         )
#     except Product.DoesNotExist:
#         return HttpResponseNotFound("product not found")
#         # return HttpResponseServerError("this company dose not exist")
#
#
# @api_view(['get'])
# def MaxPriceiApi(request, price):
#     try:
#         products = Product.objects.filter(price__lt=price)
#         serializer = HomeProductSerializer(
#             products,
#             many=True
#         )
#         return Response(
#             serializer.data
#         )
#     except Product.DoesNotExist:
#         return HttpResponseNotFound("category not found")
#         # return HttpResponseServerError("this price dose not exist")
#

@api_view(['get'])
def CategoryList(requset):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(
        categories,
        many=True
    )
    return Response(
        serializer.data
    )


@api_view(['get'])
def CompanyList(requset):
    company = Company.objects.all()
    serializer = CompanyListSerializer(
        company,
        many=True
    )
    return Response(
        serializer.data
    )


@api_view(['get'])
def ColorList(requset):
    color = Color.objects.all()
    serializer = Colorserializer(
        color,
        many=True
    )
    return Response(
        serializer.data
    )


@api_view(['GET'])
def Filter(request, category, company, color, price):
    products = Product.objects.all()
    print(products)
    print(category)
    print(company)
    print(color)
    print(price)
    if category != '-':
        try:
            category = int(category)
        except ValueError:
            pass
        else:
            products = products.filter(category=category)

        print('cat', products)
    if company != '-':
        try:
            company = int(company)
        except ValueError:
            pass
        else:
            products = products.filter(company=company)

        print('com',products)
    if color != '-':
        try:
            color = int(color)
        except ValueError:
            pass
        else:
            products = products.filter(color=color)

        print('col', products)
    if price != '-':
        try:
            price = int(price)
        except ValueError:
            pass
        else:
            products = products.filter(price__lte=price)

        print('price', products)

    serializer = HomeProductSerializer(
        products,
        many=True
    ).data

    return Response(
        serializer
    )


class HomeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image_one',
        ]


class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'image_one',
            'image_two',
            'image_three',
            'image_four',
            'image_five',
            'color_one',
            'color_two',
            'color_three',
            'color_four',
            'color_five',
            'category',
            'company',
            'category',
            'views',
        ]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'category'
        ]


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'company'
        ]


class Colorserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'color'
        ]
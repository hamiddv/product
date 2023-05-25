import random

from django.http import response , HttpResponseNotFound, HttpResponseBadRequest

from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from .models import *
from django.db.models import Max, Min


@api_view(['get'])
def AllProductApi(request):
    try:
        products = Product.objects.order_by('-price')
        serializer = HomeProductSerializer(
            products,
            many=True
        )
        return Response(
            serializer.data
        )
    except Product.DoesNotExist:
        return HttpResponseNotFound("product not found")


@api_view(['get'])
def HomeProductApi(request):
    last_id = Product.objects.latest('id').id
    first_id = Product.objects.first().id
    id_list = []
    while len(id_list) < 3:
        item = random.randint(first_id, last_id)
        if item not in id_list:
            id_list.append(item)

    product_1 = Product.objects.get(id=id_list[0])
    product_2 = Product.objects.get(id=id_list[1])
    product_3 = Product.objects.get(id=id_list[2])

    serializer1 = HomeProductSerializer(product_1).data
    serializer2 = HomeProductSerializer(product_2).data
    serializer3 = HomeProductSerializer(product_3).data

    data = [
        serializer1,
        serializer2,
        serializer3,
    ]

    return Response(data)


@api_view(['get'])
def IdProductApi(request, id):
    try:
        products = Product.objects.get(id=id)
        serializer = AllProductSerializer(
            products
        )
        products.increase_views()
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
def filterItem(request):
    color = Color.objects.all()
    serializercol = Colorserializer(
        color,
        many=True
    ).data

    company = Company.objects.all()
    serializercom = CompanyListSerializer(
        company,
        many=True
    ).data

    categories = Category.objects.all()
    serializercat = CategoryListSerializer(
        categories,
        many=True
    ).data

    products = Product.objects.order_by('-price')
    serializerprod =HomeProductSerializer(
        products,
        many=True
    ).data

    maxprice = Product.objects.aggregate(max_value=Max('price'))['max_value']
    lowest_price = Product.objects.aggregate(lowest_price=Min('price'))['lowest_price']

    res = {
            'color': serializercol,
            'company': serializercom,
            'category': serializercat,
            'products': serializerprod,
            'maxprice': maxprice,
            'lowprice': lowest_price,
    }

    return Response(
        res
    )


@api_view(['GET'])
def Filter(
        request,
        category,
        company,
        color,
        price,
        sort_by,
        free_shoping):

    check_sort_by = [
        'A',
        'Z',
        'H',
        'L'
    ]
    check_free_sopping = [
        't',
    ]

    if sort_by in check_sort_by:
        if sort_by == check_sort_by[0]:
            try:
                products = Product.objects.order_by('name')
            except ValueError:
                return HttpResponseBadRequest
            else:
                products = Product.objects.order_by('name')
        elif sort_by == check_sort_by[1]:
            try:
                products = Product.objects.order_by('-name')
            except ValueError:
                return HttpResponseBadRequest()
            else:
                products = Product.objects.order_by('-name')
        elif sort_by == check_sort_by[2]:
            try:
                products = Product.objects.order_by('-price')
            except ValueError:
                return HttpResponseBadRequest()
            else:
                products = Product.objects.order_by('-price')
        elif sort_by == check_sort_by[3]:
            try:
                products = Product.objects.order_by('price')
            except ValueError:
                return HttpResponseBadRequest()
            else:
                products = Product.objects.order_by('price')
    else:
        return HttpResponseBadRequest()


    if category != '-':
        try:
            category = int(category)
        except ValueError:
            return HttpResponseBadRequest()
        else:
            products = products.filter(category=category)

    if company != '-':
        try:
            company = int(company)
        except ValueError:
            return HttpResponseBadRequest()
        else:
            products = products.filter(company=company)

    if color != '-':
        try:
            color = int(color)
        except ValueError:
            return HttpResponseBadRequest()
        else:
            products = products.filter(color=color)

    if price != '-':
        try:
            price = int(price)
        except ValueError:
            return HttpResponseBadRequest()
        else:
            products = products.filter(price__lte=price)

    if free_shoping in check_free_sopping:
        products =products.filter(free_shoping=True)


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
            'available',
            'free_shoping',
            'image_one',
            'image_two',
            'image_three',
            'image_four',
            'image_five',
            'color',
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
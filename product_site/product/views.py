import random

from django.http import response, HttpResponseNotFound, HttpResponseBadRequest

from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from .models import *
from django.db.models import Max, Min


@api_view(['get'])
def AllProductApi(request):
    try:
        products = Product.objects.order_by('-price')
        serializer = FilterProductSerializer(
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
    serializer_list = []
    while len(serializer_list) < 3:
        item = random.randint(first_id, last_id)
        if Product.objects.filter(id=item).exists():
            product = Product.objects.get(id=item)
            serializer = HomeProductSerializer(product).data
            serializer_list.append(serializer)


    data = []
    for i in range(len(serializer_list)):
        index = i - 1
        data.append(serializer_list[index])

    return Response(data)


@api_view(['get'])
def IdProductApi(request, id):
    try:
        products = Product.objects.get(id=id)
        serializer = AllProductSerializer(
            products
        ).data

        brand = str(products.company)
        color = str(products.color)
        data = [
            serializer,
            {
                "brand": brand
            },
            {
                "color": color
            },

        ]
        products.increase_views()

        return Response(
            data
        )
    except Product.DoesNotExist:
        return HttpResponseNotFound("product not found")


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

    maxprice = Product.objects.aggregate(max_value=Max('price'))['max_value']
    lowest_price = Product.objects.aggregate(lowest_price=Min('price'))['lowest_price']

    res = {
            'color': serializercol,
            'company': serializercom,
            'category': serializercat,
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
        max_price,
        sort_by,
        free_shoping,
        search):

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
        products = Product.objects.all()
    if category != '-':
        try:
            category = int(category)
            products = products.filter(category=category)
        except ValueError:
            return HttpResponseBadRequest()
        else:
           pass

    if company != '-':
        try:
            company = int(company)
            products = products.filter(company=company)
        except ValueError:
            return HttpResponseBadRequest()

    if color != '-':
        try:
            color = int(color)
            products = products.filter(color=color)
        except ValueError:
            return HttpResponseBadRequest()

    if max_price != '-':
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            return HttpResponseBadRequest()

    if free_shoping in check_free_sopping:
        products =products.filter(free_shoping=True)

    if search != '-':
        products = products.filter(name__startswith=search)

    serializer = FilterProductSerializer(
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
            'active_image',
        ]


class FilterProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'description',
            'active_image',
        ]


class AllProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        image_sources = []
        if obj.active_image:
            image_sources.append(obj.active_image.url)
        if obj.image_two:
            image_sources.append(obj.image_two.url)
        if obj.image_three:
            image_sources.append(obj.image_three.url)
        if obj.image_four:
            image_sources.append(obj.image_four.url)
        if obj.image_five:
            image_sources.append(obj.image_five.url)
        return image_sources

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'description',
            'available',
            'free_shoping',
            'active_image',
            'images',
            'sku',
            'score',
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


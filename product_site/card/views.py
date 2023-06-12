from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .find_product_by_id import find_product_by_id
from .find_user_by_token import find_user_by_token
from .models import UserCard

from product.models import Product, Color, Company


@api_view(['POST'])
def add_card(request):
    print(request.data)
    username = request.data['username']
    token = request.data["token"]
    id = request.data["id"]
    count = request.data["count"]
    user = find_user_by_token(username, token)
    product = find_product_by_id(id)
    card = UserCard(
        user=user,
        product=product
    )
    if count is not 0:

        if user is not None:
            if product is not False:
                if product.available_count > count:
                    card = UserCard.get_or_create(
                        user=user,
                        product=product,
                    )
                    # product.available_count = product.available_count - count
                    # product.save()
                    card.save()
                    if product.available - 1 == count:
                        available = False
                    else:
                        available = True
                    print('massage : card saved')
                    return Response(
                        {
                            'massage': 'card saved',
                            'available': available,
                            'max_count': product.available_count
                        },
                        status=status.HTTP_200_OK
                    )
            else:
                print('massage: product dose not exist')
                return Response(
                    {
                        'massage': 'product dose not exist'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

    else:
        print("massage: user token not found")
        return Response(

            {
                "massage": "user token not found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def card_available(request):
    token = request.data['token']
    username = request.data['username']
    id = request.data['id']
    user = find_user_by_token(username, token)
    product = find_product_by_id(id)
    if user is not None or product is False:
        card = UserCard.objects.get(
            user=user,
            product=product,
        )

        return Response(
            {
                'count': card.count
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def get_card(request):
    username = request.data['username']
    token = request.data['token']

    user = find_user_by_token(username, token)

    if user is not None:
        card = UserCard.objects.filter(user=user)
        card_serialized = GetCardSerializers(card, many=True).data
        product_id_list = [item['product'] for item in card_serialized]

        products = Product.objects.filter(id__in=product_id_list)
        product_serialized = GetProductItem(products, many=True).data

        for item in card_serialized:
            product_id = item['product']
            product_data = next((product for product in product_serialized if product['id'] == product_id), None)
            item['product'] = product_data

        print(card_serialized)

        return Response(card_serialized, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['company']


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['color']


class GetProductItem(serializers.ModelSerializer):
    color = serializers.ReadOnlyField(source='color.color')
    company = serializers.ReadOnlyField(source='company.company')

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'score',
            'available',
            'sku',
            'color',
            'company',
            'active_image',
        ]


class GetCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = [
            'id',
            'product',
            'count',
        ]

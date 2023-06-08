from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .find_product_by_id import find_product_by_id
from .find_user_by_token import find_user_by_token
from .models import UserCard
from ..product.models import Product


@api_view(['POST'])
def add_card(request):
    token = request.headers.get("token")
    product_id = request.get("product_id")
    count = request.get("count")
    user = find_user_by_token(token)
    product_available = find_product_by_id(product_id)
    if user is not None:
        if product_available:
            card = UserCard(
                user=user,
                product=product_available,
                count=count,
            )
            card.save()
        else:
            return Response(
                {
                    'massage': 'product dose not exist'
                }
            )

    else:
        return Response(
            {
                "massage":"user token not found"
            }
        )


@api_view(['POST'])
def get_card(request):
    username = request.data['username']
    token = request.data['token']

    user = find_user_by_token(
        username,
        token
    )

    if user is not None:
        card = UserCard.objects.get(
            user=user
        )


class GetCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = [
            'product',
            'count',
        ]
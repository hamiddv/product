from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .find_product_by_id import find_product_by_id
from .find_user_by_token import find_user_by_token
from .models import UserCard
from product.models import Product


@api_view(['POST'])
def add_card(request):
    print(request.data)
    username = request.data['username']
    token = request.data["token"]
    id = request.data["id"]
    count = request.data["count"]
    user = find_user_by_token(username, token)
    product = find_product_by_id(id)
    if user is not None:
        if product is not False:
            if product.available_count > count:
                card = UserCard(
                    user=user,
                    product=product,
                    count=count,
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

        data = GetCardSerializers(
            card,
            many=True,
        ).data

        return Response(
            data,
            status=status.HTTP_200_OK
        )


class GetCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = [
            'product',
            'count',
        ]
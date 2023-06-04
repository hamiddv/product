from django.http import HttpResponse

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .find_user_by_token import get_user_from_token

from .models import UserCard
from ..product.models import Product


def add_card(request):
    token = request.headers.get("token")
    product_id = request.get("product_id")
    count = request.get("count")
    user = get_user_from_token(token)

    if user is not None:
        try:
            product_exist = Product.objects.get(id=product_id)
        except product_exist.DoesNotExist:
            return Response(
                {
                    'message': "product dose not exist"
                },
                status.HttpResponseBadRequest,
            )
        if product_exist.available:
            card = UserCard(
                product_id=product_id,
                count=count,
                user=user
            )

            card.save()
            Response(
                {
                    'massage': 'done'
                }
            )
        else:
            return Response(
                {
                    'message': 'product is not available'
                }
            )

    else:
        return HttpResponse(
            "user token not found"
        )


class AddCardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [

        ]
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser

from random import randint


@api_view(['POST'])
def create_user(request):
    if len(request.data('username')) < 8:
        return Response(
            status.HTTP_400_BAD_REQUEST
        )
    if len(request.data('password')) < 8:
        return Response(
            status.HTTP_400_BAD_REQUEST
        )

    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        ),\
            create_code_verify_email(request.data('username'))
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


def create_code_verify_email(username):
    user = CustomUser.objects.get(username=username)
    user.email_verify_code = randint(100000, 999999)


@api_view(['POST'])
def email_verify(request):
    username = request.data('username')
    email = request.data('email')
    code = request.data('code')
    user = CustomUser.objects.get(username=username)
    if code == username.email_verify_code:
        username.is_email_verified = True
        return Response(
            {
                'message': "email verified"
            },
            status.HTTP_202_ACCEPTED

        )
    else:
        Response(
            status.HTTP_406_NOT_ACCEPTABLE
        )


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                'error': 'Invalid credentials'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

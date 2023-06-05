from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser

from random import randint


@api_view(['POST'])
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


def create_code_verify_email(username):
    code = randint(100000, 999999)
    user = CustomUser.objects.get(username=username)
    user.email_verification_code = code
    user.save()


@api_view(['POST'])
def email_verify(request):
    username = request.data['username']
    email = request.data['email']
    code = request.data['code']
    new_code = request.data['new_code']

    try:
        user = CustomUser.objects.get(username=username)
    except ObjectDoesNotExist:
        return Response({'message': 'Invalid username'}, status=status.HTTP_404_NOT_FOUND)

    if code != False:
        if user.email == email:

            if new_code == True:
                create_code_verify_email(username)
                print(user.email_verify_code)
            if code == user.email_verify_code:
                user.is_email_verified = True
                user.email_verify_code = None
                user.save()
                return Response(
                    {
                        'message': 'Verification code is valid'
                    },print(user.email_verify_code)
                    ,
                    print(status=status.HTTP_200_OK)
                )
            else:
                return Response(
                    {
                        'message': 'Invalid verification code'
                    },print(user.email_verify_code)
                    ,
                    status=status.HTTP_400_BAD_REQUEST
                )


    elif code == False:
        if new_code == True:
            create_code_verify_email(username)
            return Response(
                {
                    'message' :'code creaetd'
                }, user.email_verify_code
            )





@api_view(['POST'])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
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

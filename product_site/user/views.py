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
    user.email_verify_code = code
    user.save()


@api_view(['POST'])
def email_verify(request):
    print(request.data)
    username = request.data['username']
    email = request.data['email']
    code = request.data['code']
    print('code = ' , code)
    new_code = request.data['new_code']

    try:
        user = CustomUser.objects.get(username=username)
    except ObjectDoesNotExist:
        return Response(
            {
                'message': 'Invalid username'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if new_code == True:
        create_code_verify_email(username)
        print('real code', user.email_verify_code)
        # print('new code' + new_code)

    # print('new_code' , user.email_verify_code)
    if code != False:

        if code == user.email_verify_code:
            print(user.email_verify_code)
            user.is_email_verified = True
            user.email_verify_code = None
            user.save()
            return Response(
                {
                    'message': 'Verification code is valid'
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'message': 'Invalid verification code',

                },
                status=status.HTTP_400_BAD_REQUEST
            )

    elif code == False:
        if new_code == True:
            create_code_verify_email(username)
            print(user.email_verify_code)
            return Response(
                {
                    'message': 'code created'
                },
                status=status.HTTP_200_OK
            )

    return Response(
        {
            'message': 'Invalid request'
        },
        status=status.HTTP_400_BAD_REQUEST
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

from rest_framework_simplejwt.authentication import JWTAuthentication

from product_site.user.models import CustomUser


def get_user_from_token(token):
    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
        return user
    except:
        return None
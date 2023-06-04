from rest_framework_simplejwt.authentication import JWTAuthentication
from .find_user_by_token import get_user_from_token

def my_view(request):
    token = request.headers.get("token")
    user = get_user_from_token(token)


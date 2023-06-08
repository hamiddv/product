from ..user.models import CustomUser


def find_user_by_token(username, token):
    try:
        user = CustomUser.objects.get(username=username, token=token)
    except:
        return None
    else:
        return user
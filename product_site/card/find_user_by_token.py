from user.models import CustomUser


def find_user_by_token(username, token):
    print('find_user_by_token', username, token)
    try:
        user = CustomUser.objects.get(username=username, token=token)
    except user.DoesNotExist:
        return None
    else:
        return user
from django.urls import path

from .views import create_user, login_user, email_verify, forget_password

urlpatterns = [
    path('create-user/', create_user, name='create_user'),
    path('login/', login_user, name='login_user'),
    path('verify-email/', email_verify, name='verify_email'),
    path('forget-password/', forget_password, name='forget password')

]
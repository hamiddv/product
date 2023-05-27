from django.urls import path
from .views import *

urlpatterns = [
    path(
        'api/',
        HomeProductApi
    ),

    path(
        'api/image-icon/',
        home_icon_img
    )
]
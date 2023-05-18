from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(
        "home/api/",
        HomeProductApi
    ),

    path(
        'api/category/<str:category>/',
        AllCategoryApi
    ),

    path(
        'api/company/<int:id>/',
        AllCompanyApi
    ),

    path(
        'api/price/<int:price>/',
        MaxPriceiApi
    ),

]
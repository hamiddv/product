from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(
        'filter/<str:category>/<str:company>/<str:color>/<str:max_price>/<str:sort_by>/<str:free_shoping>/<str:search>',
        Filter
    ),

    path(
        "home/api/",
        HomeProductApi
    ),

    path(
        "api/",
        AllProductApi
    ),
    #
    # path(
    #     'api/category/<str:category>/',
    #     AllCategoryApi
    # ),
    #
    # path(
    #     'api/company/<str:company>/',
    #     AllCompanyApi
    # ),

    # path(
        # 'api/price/<int:price>/',
        # MaxPriceiApi
    # ),

    path(
        'api/detail/<int:id>/',
        IdProductApi
    ),

    path(
        'api/categories-list/',
        CategoryList
    ),

    path(
        'api/companies-list/',
        CompanyList
    ),

    path(
        'api/colors-list/',
        ColorList
    ),

    path(
        'filter-item/',
        filterItem
    ),
]
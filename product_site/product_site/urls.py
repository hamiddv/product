from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'product/',
        include(
            "product.urls"
        )
    ),
    path(
        'home/',
        include(
            "home_generate.urls"
        )
    ),
    path(
        'about/',
        include(
            "about.urls"
        )
    ),
    path(
        'user/',
        include(
            "user.urls"
        )
    ),
     path(
         'card/',
         include(
             "card.urls"
         )
     )

] + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

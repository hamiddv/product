from django.urls import path

from .views import add_card, get_card

urlpatterns = [
    path(
        'add_card/',
        add_card,
        name='add card'
    ),

    path(
        'get_card/',
        get_card,
        name='get card'
    )
]
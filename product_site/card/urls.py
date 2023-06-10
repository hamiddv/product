from django.urls import path

from .views import add_card, get_card

urlpatterns = [
    path(
        'add-card/',
        add_card,
        name='add card'
    ),

    path(
        'get-card/',
        get_card,
        name='get card'
    )
]
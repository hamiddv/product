from django.urls import path

from .views import add_card, get_card, card_available


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
    ),

    path(
        'card-available/',
        card_available,
        name='card available'
    )
]

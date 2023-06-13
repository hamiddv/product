from django.db import models

from user.models import CustomUser
from product.models import Product


class UserCard(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    count = models.IntegerField(default=0)
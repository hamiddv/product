from django.db import models

from product_site.user.models import CustomUser


class UserCard(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    product = models.IntegerField()
    count = models.IntegerField()
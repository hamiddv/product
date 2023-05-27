from django.db import models


class About(models.Model):
    title = models.CharField(
        max_length=35
    )

    img = models.ImageField(
        upload_to='./media/about/'
    )

    discription = models.CharField(
        max_length=1024
    )
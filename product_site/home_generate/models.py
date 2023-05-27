from django.db import models


class HomeCustom(models.Model):
    icon = models.ImageField(
        upload_to='./media/HomeCustom/logo/img/%y/%m/%d/'
    )

    title = models.CharField(
        max_length=20
    )

    details = models.CharField(
        max_length=5024
    )

    class Meta:
        verbose_name = 'HomeCustom'
        verbose_name_plural = 'HomeCustoms'

    def __str__(self):
        return self.title


class SiteIcon(models.Model):
    icon = models.ImageField(
        upload_to='./media/site_icon/',
        null=True,
        blank=True
    )

    hero_image_one = models.ImageField(
        upload_to='./media/hero_section/',
        null=True,
        blank=True
    )

    hero_image_two = models.ImageField(
        upload_to='./media/hero_section/',
        null=True,
        blank=True
    )



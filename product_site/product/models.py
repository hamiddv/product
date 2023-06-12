from django.db import models

import datetime


class Category(models.Model):
    category = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Company(models.Model):
    company = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'


class Color(models.Model):
    color = models.CharField(max_length=6)

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'color'
        verbose_name_plural = 'colors'


class Product(models.Model):
    name = models.CharField(
        max_length=256
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    score = models.IntegerField()

    description = models.CharField(
        max_length=2024
    )

    available = models.BooleanField(
        default=False
    )

    free_shoping = models.BooleanField(
        default=False
    )

    sku = models.CharField(max_length=10)

    active_image = models.ImageField(
        upload_to="./media/product/img/%y/%m/%d/"
    )

    image_two = models.ImageField(
        upload_to="./media/product/img/%y/%m/%d/",
        null=True,
        blank=True,
    )

    image_three = models.ImageField(
        upload_to="./media/product/img/%y/%m/%d/",
        null=True,
        blank=True,
    )

    image_four = models.ImageField(
        upload_to="./media/product/img/%y/%m/%d/",
        null=True,
        blank=True,
    )
    image_five = models.ImageField(
        upload_to="./media/product/img/%y/%m/%d/",
        null=True,
        blank=True,
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    available_count = models.IntegerField(default=0)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    views = models.IntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save()

    # def __str__(self):
    #     self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'



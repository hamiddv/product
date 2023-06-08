from django.contrib.auth import authenticate

from ..product import models


def find_product_by_id(product_id):
    try:
        product = product.objects.get(id=product_id)
    except product.DoseNotExist:
        return False
    else:
        return product
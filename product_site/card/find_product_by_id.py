from django.contrib.auth import authenticate

from product.models import Product


def find_product_by_id(id):
    print('find_product_by_id', id)
    try:
        product = Product.objects.get(id=id)
    except Product.DoseNotExist:
        return False
    else:
        return product
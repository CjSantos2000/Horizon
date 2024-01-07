from .models import Product, ProductHistory


def get_product_by_id(product_id: int):
    product = Product.objects.get(id=product_id)

    return product


def get_products_by_business_id(business_id: int, limit: int = 10):
    products = Product.objects.filter(
        business__id=business_id, is_deleted=False
    ).order_by("-quantity")

    return products[0:limit]


def get_product_history_by_business_id(business_id: int):
    product_history = ProductHistory.objects.filter(business__id=business_id).order_by(
        "-created_at"
    )

    return product_history

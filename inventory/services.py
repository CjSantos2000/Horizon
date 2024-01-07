from django.utils import timezone
from business.models import Business
from .models import Product, ProductHistory


def create_product(
    name: str,
    description: str,
    price: float,
    quantity: int,
    warning_quantity: int,
    business: Business,
):
    product = Product.objects.create(
        name=name,
        description=description or None,
        price=price,
        quantity=quantity,
        warning_quantity=warning_quantity,
        business=business,
    )

    return product


def update_product(
    business: Business,
    product: Product,
    name: str,
    description: str,
    price: float,
    quantity: int,
    warning_quantity: int,
):
    product.name = name
    product.description = description or None
    product.price = price
    product.quantity = quantity
    product.warning_quantity = warning_quantity

    product.save()
    create_product_history(
        business=business,
        type="UPDATE",
        description="Updated product! \t" + "quantity: " + str(quantity),
        date_added=timezone.now(),
    )

    return product


def soft_delete_product(product_id: int):
    product = Product.objects.get(id=product_id)

    product.is_deleted = True
    product.save()

    return product


def create_product_history(
    business: Business, description: str, date_added: str, type: str
):
    product_history = ProductHistory.objects.create(
        business=business,
        description=description or None,
        type=type,
        date_added=date_added,
    )

    return product_history

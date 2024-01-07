from django.shortcuts import render

# Create your views here.
from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, FloatField
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
import business.models as business_models
from . import models

from . import selectors
from . import services


class InventoryDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        limit = None
        business = business_models.Business.objects.get(pk=pk)
        products = selectors.get_products_by_business_id(
            business_id=business.id, limit=limit
        )
        total_product_amount = (
            models.Product.objects.filter(business__id=business.id)
            .annotate(total=Sum(F("price") * F("quantity"), output_field=FloatField()))
            .values("total")
        ).aggregate(Sum("total"))

        warning_products = products.filter(quantity__lte=F("warning_quantity"))

        return render(
            request,
            "inventory/inventory-detail.html",
            context={
                "business": business,
                "inventory": products,
                "warning_products_count": warning_products.count(),
                "total_product_price": total_product_amount["total__sum"],
            },
        )

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class AddProductView(View):
    def get(self, request, pk, *args, **kwargs):
        business = business_models.Business.objects.get(pk=pk)
        context = {"user": request.user, "business": business}
        return render(request, "inventory/add-product.html", context)

    def post(self, request, pk, *args, **kwargs):
        breakpoint()
        business = business_models.Business.objects.get(pk=pk)
        name = request.POST.get("prod-name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        warning_quantity = request.POST.get("warning-quantity")
        product = services.create_product(
            business=business,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            warning_quantity=warning_quantity,
        )
        if product:
            messages.success(request, f"Product {product.name} added successfully")
            return redirect("inventory-detail", pk=business.id)

        messages.error(request, "Error adding product")
        return redirect(
            "add-product", pk=business.id, context={"fieldValues": request.POST}
        )

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class UpdateProductView(View):
    def get(self, request, pk, product_id, *args, **kwargs):
        business = business_models.Business.objects.get(pk=pk)
        product = models.Product.objects.get(pk=product_id)
        context = {"user": request.user, "business": business, "product": product}
        return render(request, "inventory/update-product.html", context=context)

    def post(self, request, pk, product_id, *args, **kwargs):
        business = business_models.Business.objects.get(pk=pk)
        product = models.Product.objects.get(pk=product_id)
        name = request.POST.get("prod-name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        warning_quantity = request.POST.get("warning-quantity")
        product = services.update_product(
            business=business,
            product=product,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            warning_quantity=warning_quantity,
        )
        if product:
            messages.success(request, f"Product {product.name} updated successfully")
            return redirect("inventory-detail", pk=business.id)

        messages.error(request, "Error updating product")
        return redirect(
            "update-product", pk=business.id, context={"fieldValues": request.POST}
        )

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class DeleteProductView(View):
    def get(self, request, pk, product_id, *args, **kwargs):
        business = business_models.Business.objects.get(pk=pk)
        product = models.Product.objects.get(pk=product_id)
        context = {"user": request.user, "business": business, "product": product}
        return render(request, "inventory/delete-product.html", context)

    def post(self, request, pk, product_id, *args, **kwargs):
        business = business_models.Business.objects.get(pk=pk)
        product = services.soft_delete_product(product_id=product_id)
        if product:
            messages.success(request, f"Product {product.name} deleted successfully")
        else:
            messages.error(request, "Error deleting product")
        return redirect("inventory-detail", pk=business.id)

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

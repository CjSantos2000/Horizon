from django.shortcuts import render

# Create your views here.
from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
import business.models as business_models
from . import models

from . import selectors
from . import services


###### TODO TEMPLATES AND FUNCTIONS ######


class InventoryDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        limit = 5
        business = business_models.Business.objects.get(pk=pk)
        products = selectors.get_products_by_business_id(business_id=pk, limit=limit)
        return render(
            request,
            "inventory/inventory-detail.html",
            context={"business": business, "transaction_logs": products},
        )

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class AddProductView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {"user": request.user}
        return render(request, "inventory/add-product.html", context)

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class EditProductView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {"user": request.user}
        return render(request, "inventory/edit-product.html", context)

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class DeleteProductView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {"user": request.user}
        return render(request, "inventory/delete-product.html", context)

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

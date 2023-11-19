from typing import Any
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from . import models

from . import selectors
from . import services


# Create your views here.


class BusinessView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            Businesses = models.Business.objects.all()
        else:
            Businesses = models.Business.objects.filter(users=request.user)
        context = {"user": request.user, "businesses": Businesses}
        return render(request, "business/index.html", context)

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class AddBusinessView(View):
    def get(self, request, *args, **kwargs):
        context = {"user": request.user}
        return render(request, "business/add-business.html", context)

    def post(self, request, *args, **kwargs):
        request.session["business_name"] = request.POST["name"]
        request.session["number_of_users"] = request.POST["number_of_users"]
        request.session["status"] = request.POST["status"]

        return redirect("add-business-users")

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class AddBusinessUsersView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()

        context = {
            "business_name": request.session["business_name"],
            "number_of_users": range(1, int(request.session["number_of_users"]) + 1),
            "status": request.session["status"],
            "users": users,
        }
        return render(request, "business/add-business-users.html", context)

    def post(self, request, *args, **kwargs):
        users_data = {
            key: value for key, value in request.POST.dict().items() if "user" in key
        }
        compressed_users_data = {
            key.split("-")[0]: {
                k.split("-")[1]: v
                for k, v in users_data.items()
                if k.startswith(key.split("-")[0] + "-")
            }
            for key in users_data
            if "-" in key
        }
        user_ids = [value["id"] for value in compressed_users_data.values()]
        total_amount = sum(
            [int(value["amount"]) for value in compressed_users_data.values()]
        )

        data = {
            value["id"]: value["amount"] for value in compressed_users_data.values()
        }

        # if user_ids have duplicate
        if len(user_ids) != len(set(user_ids)):
            messages.error(request, "Duplicate users")
            return redirect("add-business-users")

        users = selectors.get_users_by_ids_as_admin(ids=user_ids)

        business = services.create_business_as_admin(
            name=request.POST["business-name"],
            users=users,
            total_amount=total_amount,
            initial_amount=total_amount,
            status=request.POST["business-status"],
            data=data,
            created_by=request.user,
        )
        messages.success(request, f"Business {business.name} created successfully")
        return redirect("business")

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class BusinessDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        limit = 5
        business = models.Business.objects.get(pk=pk)
        transaction_logs = models.TransactionLog.objects.filter(business=business)
        return render(
            request,
            "business/business-detail.html",
            context={"business": business, "transaction_logs": transaction_logs},
        )

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class AddBusinessIncomeView(View):
    def get(self, request, pk, *args, **kwargs):
        business = models.Business.objects.get(pk=pk)
        return render(
            request, "business/add-business-income.html", context={"business": business}
        )

    def post(self, request, pk, *args, **kwargs):
        business = models.Business.objects.get(pk=pk)
        images = request.FILES.getlist("images")

        income = services.create_transaction_logs_as_admin(
            business=business,
            type=models.TransactionLog.TransactionType.INCOME,
            amount=request.POST["amount"],
            description=request.POST["description"],
            created_by=request.user,
            images=images,
        )

        if income:
            messages.success(request, "Income added successfully")
            return redirect("business-detail", pk=business.pk)

        messages.error(request, "Something went wrong")
        return redirect("add-business-income.html", pk=business.pk)

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class AddBusinessExpenseView(View):
    def get(self, request, pk, *args, **kwargs):
        business = models.Business.objects.get(pk=pk)
        return render(
            request,
            "business/add-business-expense.html",
            context={"business": business},
        )

    def post(self, request, pk, *args, **kwargs):
        business = models.Business.objects.get(pk=pk)
        images = request.FILES.getlist("images")

        expense = services.create_transaction_logs_as_admin(
            business=business,
            type=models.TransactionLog.TransactionType.EXPENSE,
            amount=request.POST["amount"],
            description=request.POST["description"],
            created_by=request.user,
            images=images,
        )

        if expense:
            messages.success(request, "Expense added successfully")
            return redirect("business-detail", pk=business.pk)

        messages.error(request, "Something went wrong")
        return redirect("add-business-expense.html", pk=business.pk)

    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class BusinessChartDataView(View):
    def get(self, request, pk, *args, **kwargs):
        period = request.GET.get("period")
        business = models.Business.objects.get(pk=pk)
        income_data, expense_data = services.get_business_chart_data(
            business=business, period=period
        )

        data = {"income": income_data, "expense": expense_data}
        return JsonResponse(data, status=200)

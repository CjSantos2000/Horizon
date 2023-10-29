from typing import Any
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


# Create your views here.


class HorizonDashboardView(View):
    @method_decorator(login_required(login_url="/authentication/login/"))
    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {"user": request.user}
        return render(request, "base.html", context)

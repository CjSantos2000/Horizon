import json
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

from . import models, selectors

# Create your views here.

""" [TODO] -> Transfer to class based views """


def index(request):
    currency_file_path = os.path.join(settings.BASE_DIR, "currencies.json")

    currency_data = selectors.get_currencies_from_json(currency_file_path)

    exists = models.UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None

    if exists:
        user_preferences = models.UserPreference.objects.get(user=request.user)

    context = {"currencies": currency_data, "user_preferences": user_preferences}

    if request.method == "GET":
        # # Will pause the code in the set trace line and can test or check the value of the variable or the flow of the code
        # import pdb

        # pdb.set_trace()

        return render(
            request,
            "preferences/index.html",
            context,
        )
    elif request.method == "POST":
        currency = request.POST["currency"]
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            models.UserPreference.objects.create(user=request.user, currency=currency)

        messages.success(request, "Changes saved")
        return render(
            request,
            "preferences/index.html",
            context,
        )

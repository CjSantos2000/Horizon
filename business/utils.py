from django.db.models import QuerySet
from collections import defaultdict


def format_chart_data(queryset: QuerySet):
    data_dict_income = {"labels": [], "data": []}
    data_dict_expense = {"labels": [], "data": []}
    for entry in queryset:
        data_dict_income["labels"].append(entry["date"])
        data_dict_income["data"].append(float(entry["income_total_amount"]))

        data_dict_expense["labels"].append(entry["date"])
        data_dict_expense["data"].append(float(entry["expense_total_amount"]))

    return data_dict_income, data_dict_expense


from math import ceil


def week_of_month(date):
    """Returns the week of the month for the specified date."""

    first_day = date.replace(day=1)

    dom = date.day
    adjusted_dom = dom + (1 + first_day.weekday()) % 7

    return int(ceil(adjusted_dom / 7.0))


def compress_monthly_data(data):
    combined_data = defaultdict(float)
    for label, amount in zip(data["labels"], data["data"]):
        combined_data[week_of_month(label)] += amount
    return dict(combined_data)

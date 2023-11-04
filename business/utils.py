from django.db.models import QuerySet


def format_chart_data(queryset: QuerySet):
    data_dict = {"labels": [], "data": []}
    for entry in queryset:
        data_dict["labels"].append(entry["date"])
        data_dict["data"].append(
            float(entry["income_total_amount"] - float(entry["expense_total_amount"]))
        )
    return data_dict


from math import ceil


def week_of_month(date):
    """Returns the week of the month for the specified date."""

    first_day = date.replace(day=1)

    dom = date.day
    adjusted_dom = dom + (1 + first_day.weekday()) % 7

    return int(ceil(adjusted_dom / 7.0))

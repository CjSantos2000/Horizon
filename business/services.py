import calendar
from datetime import datetime, timedelta, date
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.files import File
from django.db import transaction
from django.db.models import F, Sum, Case, When, Value
from django.db.models.fields import FloatField
from typing import List, Dict, Any
from authentication.selectors import get_user_by_username
from HorizonApp import errors
from .models import Business, BusinessContribution, TransactionLog, TransactionFile
from .utils import format_chart_data, week_of_month, compress_monthly_data


def create_business_as_admin(
    name: str,
    users: List[User],
    total_amount: Decimal,
    initial_amount: Decimal,
    status: str,
    data: Dict[str, Any],
    created_by: User,
) -> Business:
    """
    This function receives a request data and creates a business as admin.
    @params name (str): The name of business.
    @params users (List[User]): The users.
    @params total_amount (Decimal): The total amount.
    @params status (str): The status.
    @params data (Dict[str, Any]): The data.
    @out (Business): The created business.
    """
    if not created_by.is_superuser:
        error_code, error_msg = errors.USER_NO_ACCESS
        raise errors.InvestorAppException(error_msg, code=error_code)

    if len(users) > 10:
        error_code, error_msg = errors.REACHED_MAX_USERS_ON_BUSINESS
        raise errors.InvestorAppException(error_msg, code=error_code)

    business_status = {
        "active": Business.Status.ACTIVE,
        "inactive": Business.Status.INACTIVE,
    }
    business = Business.objects.create(
        name=name,
        total_amount=total_amount,
        status=business_status[status],
        data=data,
        initial_amount=initial_amount,
    )

    if users:
        business.users.set(users)

    for user in business.users.all():
        create_user_business_contribution(
            name=f"{user.username} Business Contributor",
            business=business,
            user=user,
        )

    return business


def create_user_business_contribution(
    name: str,
    business: Business,
    user: User,
) -> BusinessContribution:
    """
    This function receives a request data and creates a user business contribution.
    @params name (str): The name of business contributor.
    @params business (Business): The business.
    @params user (User): The user.
    """
    amount = business.data.get(f"{user.id}")
    percentage = (int(business.data.get(f"{user.id}")) / business.total_amount) * 100

    return BusinessContribution.objects.create(
        name=name,
        business=business,
        user=user,
        amount=amount,
        percentage=percentage,
    )


def create_transaction_logs_as_admin(
    business: Business,
    type: str,
    description: str,
    amount: Decimal,
    created_by: User,
    images: List[any],
    custom_created_at_date: date,
) -> TransactionLog:
    """
    This function receives a request data and creates a transaction log as admin.
    @params transaction_id (str): The transaction id.
    @params type (str): The type.
    @params business (Business): The business.
    @params amount (Decimal): The amount.
    @params created_by (User): The created by.
    """
    if not created_by.is_superuser:
        error_code, error_msg = errors.USER_NO_ACCESS
        raise errors.InvestorAppException(error_msg, code=error_code)

    try:
        with transaction.atomic():
            transaction_obj = TransactionLog.objects.create(
                type=type,
                business=business,
                amount=Decimal(amount),
                description=description,
                created_by=created_by,
                custom_created_at_date=custom_created_at_date,
            )

            if transaction_obj:
                update_business_total_amount_via_transaction_log(
                    business=business, transaction_log=transaction_obj
                )

                for image in images:
                    file_name = image._name
                    file_type = image.content_type
                    # TODO - Add file size validation and file path location
                    transaction_file = TransactionFile.objects.create(
                        transaction_log=transaction_obj,
                        file_name=file_name,
                        file_type=file_type,
                    )
                    transaction_file.file.save(file_name, File(image))

    except Exception as e:
        error_code, error_msg = errors.TRANSACTION_LOG_CREATE_FAILED
        raise errors.InvestorAppException(error_msg, code=error_code)

    return transaction_obj


def update_business_total_amount_via_transaction_log(
    business: Business,
    transaction_log: TransactionLog,
) -> Business:
    """
    This function receives a request data and updates the business total amount.
    @params business (Business): The business.
    @params transactionlog (TransactionLog): The transaction log.
    @out (Business): The updated business.
    """

    with transaction.atomic():
        if transaction_log.type == TransactionLog.TransactionType.INCOME:
            business.total_amount += transaction_log.amount
        elif transaction_log.type == TransactionLog.TransactionType.EXPENSE:
            business.total_amount -= transaction_log.amount

        business.save()

    return business


def get_business_chart_data(*, business: Business, period: str):
    """
    This function receives a request data and returns the business chart data.
    @params business (Business): The business.
    @params period (str): The period.
    @out (Dict[str, Any]): The business chart data.

    """
    # Get the current date
    current_date = datetime.now()
    queryset = TransactionLog.objects.filter(business=business).exclude(
        description="Initial Investment"
    )
    date = F("custom_created_at_date")

    if period == "all":
        # Calculate the start and end dates for this week, this month, and this year
        queryset = queryset
    elif period == "weekly":
        # Calculate the start and end dates for this week, this month, and this year
        start_of_week = current_date - timedelta(days=current_date.weekday() + 1)
        end_of_week = start_of_week + timedelta(days=6)
        queryset = queryset.filter(
            custom_created_at_date__range=[start_of_week, end_of_week],
        )
    elif period == "monthly":
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(
            day=calendar.monthrange(current_date.year, current_date.month)[1]
        )

        queryset = queryset.filter(
            custom_created_at_date__range=[start_of_month, end_of_month],
        )
    elif period == "yearly":
        start_of_year = current_date.replace(month=1, day=1)
        date = F("custom_created_at_date__month")
        queryset = queryset.filter(
            custom_created_at_date__range=[start_of_year, current_date],
        )

    queryset = queryset.values(date=date).annotate(
        income_total_amount=Sum(
            Case(
                When(type=TransactionLog.TransactionType.INCOME, then=F("amount")),
                default=Value(0),
                output_field=FloatField(),
            )
        ),
        expense_total_amount=Sum(
            Case(
                When(type=TransactionLog.TransactionType.EXPENSE, then=F("amount")),
                default=Value(0),
                output_field=FloatField(),
            )
        ),
    )

    income, expense = format_chart_data(queryset=queryset)

    income_data = income
    expense_data = expense

    if period == "monthly":
        compressed_income_data = compress_monthly_data(income_data)
        compressed_expense_data = compress_monthly_data(expense_data)
        income_result = {
            "labels": [key for key in compressed_income_data.keys()],
            "data": [value for value in compressed_income_data.values()],
        }
        expense_result = {
            "labels": [key for key in compressed_expense_data.keys()],
            "data": [value for value in compressed_expense_data.values()],
        }

        income_data = {
            "labels": [f"Week {label}" for label in income_result["labels"]],
            "data": income_result["data"],
        }
        expense_data = {
            "labels": [f"Week {label}" for label in expense_result["labels"]],
            "data": expense_result["data"],
        }
    elif period == "yearly":
        income_data = {
            "labels": [calendar.month_name[label] for label in income["labels"]],
            "data": income["data"],
        }
        expense_data = {
            "labels": [calendar.month_name[label] for label in expense["labels"]],
            "data": expense["data"],
        }

    return income_data, expense_data

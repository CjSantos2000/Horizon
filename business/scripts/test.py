import pandas as pd
from datetime import datetime
from django.contrib.auth.models import User
from ..models import Business, TransactionLog
from ..services import create_transaction_logs_as_admin


def run():
    user = User.objects.filter(is_superuser=True).first()
    business = Business.objects.get(name="Mangkok Meals & Sizzlig")
    df = pd.read_csv("business/scripts/Initial-sales.csv")
    for index, row in df.iterrows():
        print(f"Row {index + 1}:")
        print(row["Date"])
        print(row["Type"])
        print(row["Description"])
        print(row["Amount"])
        print("-" * 20)
        custom_created_at_date = datetime.strptime(row["Date"], "%d/%m/%Y").date()

        if row["Type"] == "INCOME":
            transaction_type = TransactionLog.TransactionType.INCOME
        else:
            transaction_type = TransactionLog.TransactionType.EXPENSE

        create_transaction_logs_as_admin(
            business=business,
            type=transaction_type,
            description=row["Description"],
            amount=row["Amount"],
            created_by=user,
            images=[],
            custom_created_at_date=custom_created_at_date,
        )

    print("Done!")

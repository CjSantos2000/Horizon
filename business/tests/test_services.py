from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Business, BusinessContribution, TransactionLog
from ..services import (
    create_business_as_admin,
    create_user_business_contribution,
    create_transaction_logs_as_admin,
)


# Create unit tests for all the services in core\services.py
class TestServices(TestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(
            username="testuser", password="12345", is_superuser=True
        )
        self.user = User.objects.create_user(
            username="testuser1", password="12345", is_superuser=False
        )

        self.business = create_business_as_admin(
            name="Test Business",
            users=[self.user, self.user_admin],
            total_amount=1000.00,
            status=Business.Status.ACTIVE,
            data={self.user.id: 50, self.user_admin.id: 50},
            initial_amount=1000.00,
            created_by=self.user_admin,
        )

    def test_create_business_as_admin_when_invalid(self):
        """Test create business service."""
        with self.assertRaises(Exception):
            create_business_as_admin(
                name="Test Business",
                users=[self.user, self.user_admin],
                total_amount=1000.00,
                status=Business.Status.ACTIVE,
                data={self.user.id: 50, self.user_admin.id: 50},
                created_by=self.user,
            )

    def test_create_business_as_admin_when_no_users_valid(self):
        """Test create business service."""
        business = create_business_as_admin(
            name="Test Business",
            users=[],
            total_amount=1000.00,
            initial_amount=1000.00,
            status=Business.Status.ACTIVE,
            data={self.user.id: 50, self.user_admin.id: 50},
            created_by=self.user_admin,
        )
        self.assertEqual(business.name, "Test Business")
        self.assertEqual(business.users.count(), 0)
        self.assertEqual(business.total_amount, 1000.00)
        self.assertEqual(business.status, Business.Status.ACTIVE)
        self.assertEqual(business.data[self.user.id], 50)

    def test_create_business_as_admin_when_valid(self):
        """Test create business service."""
        business = create_business_as_admin(
            name="Test Business",
            users=[self.user, self.user_admin],
            total_amount=1000.00,
            initial_amount=1000.00,
            status=Business.Status.ACTIVE,
            data={self.user.id: 50, self.user_admin.id: 50},
            created_by=self.user_admin,
        )
        self.assertEqual(business.name, "Test Business")
        self.assertEqual(business.users.count(), 2)
        self.assertEqual(business.total_amount, 1000.00)
        self.assertEqual(business.status, Business.Status.ACTIVE)
        self.assertEqual(business.data[self.user.id], 50)

    def test_create_business_contribution_when_valid(self):
        """Test create business contribution service."""
        user_business_contribution = create_user_business_contribution(
            name="Test User Business Contribution",
            business=self.business,
            user=self.business.users.last(),
        )
        self.assertEqual(
            user_business_contribution.name, "Test User Business Contribution"
        )
        self.assertEqual(user_business_contribution.business, self.business)
        self.assertEqual(user_business_contribution.user, self.user)
        self.assertEqual(user_business_contribution.amount, 500.00)
        self.assertEqual(user_business_contribution.percentage, 50)

    def test_create_transaction_logs_income_when_not_superuser(self):
        """Test create transaction logs service."""
        with self.assertRaises(Exception):
            create_transaction_logs_as_admin(
                transaction_id="Test Transaction ID",
                type=TransactionLog.TransactionType.INCOME,
                business=self.business,
                amount=1000.00,
                created_by=self.user,
            )

    def test_create_transaction_logs_income_when_valid(self):
        """Test create transaction logs service."""

        transaction_logs = create_transaction_logs_as_admin(
            transaction_id="Test Transaction ID",
            type=TransactionLog.TransactionType.INCOME,
            business=self.business,
            amount=1000.00,
            created_by=self.user_admin,
        )

        self.assertEqual(transaction_logs.transaction_id, "Test Transaction ID")
        self.assertEqual(transaction_logs.type, TransactionLog.TransactionType.INCOME)
        self.assertEqual(transaction_logs.business, self.business)
        self.assertEqual(transaction_logs.amount, 1000.00)
        self.assertEqual(transaction_logs.created_by, self.user_admin)
        self.assertEqual(self.business.total_amount, 2000.00)

    def test_create_transaction_logs_expense_when_invalid(self):
        """Test create transaction logs service."""
        with self.assertRaises(Exception):
            create_transaction_logs_as_admin(
                transaction_id="Test Transaction ID",
                type=TransactionLog.TransactionType.EXPENSE,
                business=self.business,
                amount=1000.00,
                created_by=self.user,
            )

    def test_create_transaction_logs_expense_when_valid(self):
        """Test create transaction logs service."""

        transaction_logs = create_transaction_logs_as_admin(
            transaction_id="Test Transaction ID",
            type=TransactionLog.TransactionType.EXPENSE,
            business=self.business,
            amount=1000.00,
            created_by=self.user_admin,
        )

        self.assertEqual(transaction_logs.transaction_id, "Test Transaction ID")
        self.assertEqual(transaction_logs.type, TransactionLog.TransactionType.EXPENSE)
        self.assertEqual(transaction_logs.business, self.business)
        self.assertEqual(transaction_logs.amount, 1000.00)
        self.assertEqual(transaction_logs.created_by, self.user_admin)
        self.assertEqual(self.business.total_amount, 0.00)

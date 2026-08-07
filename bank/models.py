from django.db import models
from django.contrib.auth.models import User


class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, unique=True)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("Deposit", "Deposit"),
        ("Withdraw", "Withdraw"),
    ]

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_type 
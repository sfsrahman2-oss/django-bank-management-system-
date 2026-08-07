import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import BankAccount, Transaction
from .forms import BankAccountForm, DepositForm, WithdrawForm
from django.db.models import Sum
from django.http import HttpResponse
@login_required
def dashboard(request):
    account = BankAccount.objects.filter(user=request.user).first()

    total_deposits = 0
    total_withdrawals = 0
    total_transactions = 0

    if account:
        total_deposits = (
            Transaction.objects.filter(
                account=account,
                transaction_type="Deposit"
            ).aggregate(Sum("amount"))["amount__sum"] or 0
        )

        total_withdrawals = (
            Transaction.objects.filter(
                account=account,
                transaction_type="Withdraw"
            ).aggregate(Sum("amount"))["amount__sum"] or 0
        )

        total_transactions = Transaction.objects.filter(
            account=account
        ).count()

    return render(request, "bank/dashboard.html", {
        "account": account,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "total_transactions": total_transactions,
    }) 


@login_required
def create_account(request):
    if request.method == "POST":
        form = BankAccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect("dashboard")
    else:
        form = BankAccountForm()

    return render(request, "bank/create_account.html", {
        "form": form,
    }) 
@login_required
def deposit(request):
    account = BankAccount.objects.get(user=request.user)

    if request.method == "POST":
        form = DepositForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            account.current_balance += amount
            account.save()

            Transaction.objects.create(
                account=account,
                transaction_type="Deposit",
                amount=amount,
                balance_after_transaction=account.current_balance,
            )

            messages.success(request, "Money deposited successfully!")
            return redirect("dashboard")
    else:
        form = DepositForm()

    return render(request, "bank/deposit.html", {"form": form}) 
@login_required
def withdraw(request):
    account = BankAccount.objects.get(user=request.user)

    if request.method == "POST":
        form = WithdrawForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            if amount > account.current_balance:
                messages.error(request, "Insufficient balance!")
            else:
                account.current_balance -= amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    transaction_type="Withdraw",
                    amount=amount,
                    balance_after_transaction=account.current_balance,
                )

                messages.success(request, "Money withdrawn successfully!")
                return redirect("dashboard")
    else:
        form = WithdrawForm()

    return render(request, "bank/withdraw.html", {"form": form})
@login_required
def export_csv(request):
    account = BankAccount.objects.get(user=request.user)

    transactions = Transaction.objects.filter(
        account=account
    ).order_by("-created_at")

    response = HttpResponse(
        content_type="text/csv"
    )

    response["Content-Disposition"] = (
        'attachment; filename="transaction_history.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        "Transaction Type",
        "Amount",
        "Date & Time",
        "Balance After Transaction"
    ])

    for transaction in transactions:
        writer.writerow([
            transaction.transaction_type,
            transaction.amount,
            transaction.created_at,
            transaction.balance_after_transaction
        ])

    return response
@login_required
def transaction_history(request):
    account = BankAccount.objects.get(user=request.user)

    transactions = Transaction.objects.filter(account=account)

    transaction_type = request.GET.get("type")
    date = request.GET.get("date")

    if transaction_type:
        transactions = transactions.filter(
            transaction_type__icontains=transaction_type
        )

    if date:
        transactions = transactions.filter(
            created_at__date=date
        )

    transactions = transactions.order_by("-created_at")

    return render(request, "bank/transaction_history.html", {
        "transactions": transactions,
    }) 
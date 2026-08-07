from django import forms
from .models import BankAccount


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [
            "account_holder_name",
            "account_number",
        ]

        widgets = {
            "account_holder_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter account holder name",
                }
            ),
            "account_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter account number",
                }
            ),
        }


class DepositForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0.01,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter amount",
                "step": "0.01",
            }
        ),
    )


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0.01,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter amount",
                "step": "0.01",
            }
        ),
    ) 
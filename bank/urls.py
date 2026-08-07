from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create-account/", views.create_account, name="create_account"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transactions/", views.transaction_history, name="transaction_history"),
    path("export-csv/", views.export_csv, name="export_csv"),
] 
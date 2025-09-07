from django.urls import path
from . import views

urlpatterns = [
    path('wallets/<uuid:wallet_id>/', views.WalletDetailView.as_view(), name='wallet-detail'),
    path('wallets/<uuid:wallet_id>/operation/', views.TransactionCreateView.as_view(), name='wallet-operation'),
]

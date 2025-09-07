from django.contrib import admin

from wallets.models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Админ - панель для кошелька"""
    list_display = ('id', 'balance')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Админ - панель для операций"""
    list_display = ('id', 'wallet', 'amount')

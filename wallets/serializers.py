from rest_framework import serializers
from decimal import Decimal
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    """Сериализатор для кошелька"""
    class Meta:
        """Метаданные"""
        model = Wallet
        fields = ['id', 'balance']
        read_only_fields = ['id', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    """Сериализатор для транзакции"""
    class Meta:
        """Метаданные"""
        model = Transaction
        fields = ['operation_type', 'amount']

    def validate_amount(self, value):
        """Валидация суммы транзакции"""
        if value <= Decimal('0.00'):
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        """Валидация всей транзакции"""
        # Получаем кошелек из контекста
        wallet = self.context.get('wallet')
        if not wallet:
            raise serializers.ValidationError("Wallet not provided in context")

        operation_type = data.get('operation_type')
        amount = data.get('amount')

        if operation_type == 'WITHDRAW' and amount:
            if wallet.balance < amount:
                raise serializers.ValidationError("Insufficient funds.")
        return data

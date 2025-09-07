import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator

from django.db import models


class Wallet(models.Model):
    """Модель - Кошелек"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'),
                                  validators=[MinValueValidator(Decimal('0.00'))], verbose_name='баланс')
    created_ad = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_ad = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        """Метаданные"""
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'

    def __str__(self):
        return f'Кошелек {self.pk} - {self.balance} руб.'


class Transaction(models.Model):
    """Модель - Операции"""
    OPERATION_CHOISES = [
        ('DEPOSIT', 'Пополнение'),
        ('WITHDRAW', 'Снятие')
    ]
    wallet = models.ForeignKey(Wallet, models.CASCADE, verbose_name='Кошелек')
    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOISES, verbose_name='Тип операции',
                                      help_text='Выберите тип операции')
    created_ad = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        """Метаданные"""
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'Операция: {self.operation_type}, сумма - {self.amount}'

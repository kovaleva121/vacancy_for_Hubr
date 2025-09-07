from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Wallet
import uuid


class WalletTests(APITestCase):
    def setUp(self):
        """Создание тестовых объектов"""
        self.wallet = Wallet.objects.create(balance=1000.00)
        self.wallet_url = reverse('wallet-detail', kwargs={'wallet_id': self.wallet.id})
        self.operation_url = reverse('wallet-operation', kwargs={'wallet_id': self.wallet.id})

    def test_get_wallet_balance(self):
        """Отображение детали кошелька"""
        response = self.client.get(self.wallet_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '1000.00')

    def test_get_nonexistent_wallet(self):
        """Ошибка отображения деталей несуществующего кошелька"""
        fake_id = uuid.uuid4()
        url = reverse('wallet-detail', kwargs={'wallet_id': fake_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deposit_operation(self):
        """Проверка транзакции пополнения кошелька"""
        data = {
            'operation_type': 'DEPOSIT',
            'amount': '500.00'
        }
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wallet = Wallet.objects.get(id=self.wallet.id)
        self.assertEqual(wallet.balance, 1500.00)

    def test_withdraw_operation(self):
        """Проверка транзакции снятия денег с кошелька"""
        data = {
            'operation_type': 'WITHDRAW',
            'amount': '300.00'
        }
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wallet = Wallet.objects.get(id=self.wallet.id)
        self.assertEqual(wallet.balance, 700.00)

    def test_withdraw_insufficient_funds(self):
        """Проверка на валидацию превышения суммы"""
        data = {
            'operation_type': 'WITHDRAW',
            'amount': '1500.00'
        }
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_operation_type(self):
        """Проверка на несуществующую транзакцию"""
        data = {
            'operation_type': 'INVALID',
            'amount': '100.00'
        }
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_amount(self):
        """Проверка валидации на пополнение отрицательной суммы"""
        data = {
            'operation_type': 'DEPOSIT',
            'amount': '-100.00'
        }
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_zero_amount(self):
        """Проверка валидации на пополнение 0 суммы"""
        data = {
            'operation_type': 'DEPOSIT',
            'amount': '0.00'
        }
        response = self.client.post(self.operation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletDetailView(generics.RetrieveAPIView):
    """Контроллер получения детальной информации кошелька"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'wallet_id'


class TransactionCreateView(generics.CreateAPIView):
    """Контроллер создания транзакции"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_wallet(self):
        """Получение кошелька"""
        wallet_id = self.kwargs['wallet_id']
        return get_object_or_404(Wallet, id=wallet_id)

    def perform_create(self, serializer):
        """Бизнес-логика создания транзакции"""
        wallet = self.get_wallet()

        with transaction.atomic():
            # Блокируем запись кошелька для предотвращения race condition
            wallet = Wallet.objects.select_for_update().get(id=wallet.id)

            operation_type = serializer.validated_data['operation_type']
            amount = serializer.validated_data['amount']

            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            elif operation_type == 'WITHDRAW':
                if wallet.balance < amount:
                    raise serializers.ValidationError("Insufficient funds.")
                wallet.balance -= amount

            wallet.save()
            serializer.save(wallet=wallet)

    def create(self, request, *args, **kwargs):
        """Основное создание объекта"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except serializers.ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Операция успешно выполнена'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_serializer_context(self):
        """Добавляем кошелек в контекст"""
        context = super().get_serializer_context()
        context['wallet'] = self.get_wallet()
        return context

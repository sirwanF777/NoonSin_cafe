from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Sum, Q, Count
from django.db.models.functions import Coalesce


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVED = 3
    TRANSFER_SENT = 4

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (TRANSFER_RECEIVED, "Transfer Received"),
        (TRANSFER_SENT, "Transfer Sent"),
    )

    user = models.ForeignKey(
        User, related_name="transactions", on_delete=models.RESTRICT
    )
    transaction_type = models.PositiveIntegerField(
        choices=TRANSACTION_TYPE_CHOICES, default=CHARGE,
    )
    amount = models.BigIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_report(cls):
        """Show all users and their balances."""
        positive_transactions = Sum(
            'transactions__amount',
            filter=Q(transactions__transaction_type__in=(1, 3))
        )
        negative_transactions = Sum(
            'transaction__amount',
            filter=Q(transactions__transaction_type__in=(2, 4))
        )

        users = User.objects.all().annotate(
            transactions_count=Count('transactions__id'),
            balance=Coalesce(positive_transactions, 0)-Coalesce(negative_transactions, 0)
        )

        return users

    @classmethod
    def get_total_balance(cls):
        query_set = cls.get_report()
        return query_set.aggregate(Sum('balance'))

    @classmethod
    def user_balance(cls):
        positive_transactions = Sum(
            'amount',
            filter=Q(transaction_type__in=(1, 3))
        )
        negative_transactions = Sum(
            'amount',
            filter=Q(transaction_type__in=(2, 4))
        )

        user_balance = User.objects.all().aggregate(
            balance=Coalesce(positive_transactions, 0)-Coalesce(negative_transactions, 0)
        )

        return user_balance.get('balance', 0)

    def __str__(self):
        return f"{self.user} - {self.transaction_type} - {self.amount}"


class UserBalance(models.Model):
    user = models.ForeignKey(
        User, related_name="balance_records", on_delete=models.RESTRICT,
    )
    balance = models.BigIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def record_user_balance(cls, user):
        balance = Transaction.user_balance(user)
        instance = cls.objects.create(user=user, balance=balance)
        return instance

    @classmethod
    def record_all_users_balance(cls):
        users = User.objects.all()
        records = list()
        for user in users:
            records.append(cls.record_user_balance(user))

        return set(records)

    def __str__(self):
        return f"{self.user} - {self.balance}"


class TransferTransaction(models.Model):
    sender_transaction = models.ForeignKey(
        Transaction, related_name='sender_transfer', on_delete=models.RESTRICT,
    )
    receiver_transaction = models.ForeignKey(
        Transaction, related_name="receiver_transfer", on_delete=models.RESTRICT,
    )
    amount_transaction = models.BigIntegerField()

    @classmethod
    def transfer(cls, sender, receiver, amount):
        if Transaction.user_balance(sender) < amount:
            return "transaction not Allowed. insufficient balance."

        with transaction.atomic():
            sender_transaction = Transaction.objects.create(
                user=sender, transaction_type=Transaction.TRANSFER_SENT, amount=amount
            )
            receiver_transaction = Transaction.objects.create(
                user=receiver, transaction_type=Transaction.TRANSFER_RECEIVED, amount=amount
            )

            instance = cls.objects.create(
                sender_transaction=sender_transaction, receiver_transaction=receiver_transaction,
                amount_transaction=amount
            )

        return instance

    def __str__(self):
        return f"{self.sender_transaction} to {self.received_transaction}"

from django.contrib import admin
from django.contrib.admin import register
from transaction.models import *


@register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'create_time')
    search_fields = ('user__name', )
    list_filter = ('transaction_type', )


@register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'create_time')
    search_fields = ('user__name', )

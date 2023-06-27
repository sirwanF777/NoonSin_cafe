from django.contrib import admin
from django.contrib.admin import register
from catalogue.models import Category, Product, Table, Hall


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'pattern', 'create_time', 'modified_time']
    search_fields = ['name']
    list_editable = ['pattern']
    list_filter = ['pattern']


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'upc', 'title', 'price', 'category', 'is_active',
        'create_time', 'modified_time'
    ]
    list_filter = ['category']
    list_editable = ['price', 'category', 'is_active']
    search_fields = ['title', 'price', 'is_active']


@register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = [
        'table_number', 'table_capacity', 'price', 'create_time', 'modified_time'
    ]
    list_filter = ['table_capacity']
    list_editable = ['price', 'table_capacity']
    search_fields = ['price', 'table_capacity']


@register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['hall_number', 'name', 'create_time', 'modified_time']
    search_fields = ['name', 'hall_number']

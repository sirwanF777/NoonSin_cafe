from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)
    pattern = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    create_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    upc = models.IntegerField(unique=True)
    title = models.CharField(max_length=32, verbose_name='title')
    price = models.FloatField(verbose_name="price")
    description = models.TextField(null=True, blank=True, verbose_name="description")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='category',
        related_name='products'
    )
    is_active = models.BooleanField(default=False)
    create_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = 'products'

    def __str__(self):
        return f"title: {self.title} to price: {self.price}"


class Table(models.Model):
    upc = models.IntegerField(unique=True)
    table_number = models.IntegerField(verbose_name="table_number", unique=True)
    table_capacity = models.IntegerField(default=4)
    price = models.FloatField(verbose_name="price")
    description = models.TextField(null=True, blank=True, verbose_name="description")
    create_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "table"
        verbose_name_plural = 'tables'

    def __str__(self):
        return f"number: {self.table_number} to price: {self.price} " \
               f"-> table capacity: {self.table_capacity}"


class Hall(models.Model):
    name = models.CharField(max_length=32)
    hall_number = models.IntegerField(unique=True)
    description = models.TextField(null=True, blank=True)
    create_time = models.DateField(auto_now_add=True)
    modified_time = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "hall"
        verbose_name_plural = "halls"

    def __str__(self):
        return f"name: {self.name} \t number: {self.hall_number}"

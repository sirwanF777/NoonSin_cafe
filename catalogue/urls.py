from django.urls import path, re_path
from catalogue.views import *

urlpatterns = [
    path('product-list/', product_list, name="product-list"),
    path('product-detail/<int:upc>/', product_detail, name="product-detail"),
    path('product/search/', products_search, name='product-search'),
    path('category-list/', category_list, name='category-list'),
    path('category/<int:pk>/products/', category_products, name="category-detail"),
    path('table-list/', table_list, name="table-list"),
    path('table-detail/<int:upc>/', table_detail, name="table-detail"),
    path('hall-list/', hall_list, name="hall-list"),
    path('hall-detail/<int:pk>/', hall_detail, name="hall-detail"),
]
